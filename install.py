import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

from src.engine_utils.directory_info import DirectoryInfo

# Packages that were previously handled specially for MuseTalk (OpenMMLab stack).
# Now empty: mmcv/mmpose/mmdet/mmengine replaced by ONNX Runtime in musetalk.
MUSETALK_SPECIAL_PKGS: set = set()

# Known version overrides: when multiple handlers declare conflicting pins,
# use these tested-compatible versions instead.
VERSION_OVERRIDES = {
    "numpy": "==1.26.4",
    "opencv-python": "==4.9.0.80",
    "pillow": ">=11.1.0,<12.0",
    "transformers": "==4.44.2",
    # TensorFlow 2.16.x requires protobuf < 5.0; keep this pinned so
    # uv/pip resolution won't upgrade to protobuf 7.x.
    "protobuf": ">=4.25.3,<5",
    # xfuser>=0.4.3 and FlashHead need accelerate>=0.33.0 / >=1.8.1,
    # which conflicts with musetalk's ~=0.28.0 pin.
    "accelerate": ">=1.8.1",
    # FlashHead needs diffusers>=0.34.0, conflicting with
    # musetalk/cosyvoice's ~=0.30.2 pin.
    # Upper-bound <0.36.0 avoids Dinov2WithRegistersConfig import that
    # requires transformers>=4.57 (OAC pins 4.44.2).
    "diffusers": ">=0.34.0,<0.36.0",
}

# Package name replacements: when handler pyproject.toml declares a CPU-only
# package but the project should use the GPU variant instead.
PACKAGE_REPLACEMENTS = {
    "onnxruntime": "onnxruntime-gpu",
}

# Packages managed by the root pyproject.toml that must NEVER be overridden
# by handler dependencies. These are injected into the install list with
# pinned versions to prevent transitive deps (e.g. xformers -> torch) from
# downgrading them.
PROTECTED_PACKAGES = {
    "torch": "==2.8.0",
    "torchvision": "==0.23.0",
    "torchaudio": "==2.8.0",
}

# Packages that require --no-build-isolation (they use pkg_resources or
# other build-time dependencies not declared in their build-system.requires)
NO_BUILD_ISOLATION_PKGS = {"openai-whisper", "flash-attn"}

# Maximum parallel compilation jobs for packages that build from source
# (e.g. flash-attn). Set low to avoid OOM / server crash on shared machines.
MAX_COMPILE_JOBS = 4


def parse_args():
    parser = argparse.ArgumentParser(
        description="One-stop dependency installer for OpenAvatarChat. "
                    "Reads config YAML(s) to determine which handlers are needed, "
                    "then installs all dependencies in one pass."
    )
    parser.add_argument(
        "--config", type=str, action="append", dest="configs",
        help="Path to config file (can be specified multiple times)"
    )
    parser.add_argument(
        "--all", action="store_true", dest="install_all",
        help="Install dependencies for ALL handlers"
    )
    parser.add_argument(
        "--skip-core", action="store_true",
        help="Skip installation of core project dependencies"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be installed without actually installing"
    )
    return parser.parse_args()


def is_venv_active():
    return (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
        or os.getenv("VIRTUAL_ENV") is not None
    )


def load_yaml(config_path: str) -> dict:
    base_dir = DirectoryInfo.get_project_dir()
    path = Path(config_path) if os.path.isabs(config_path) else Path(base_dir) / config_path
    if not path.exists():
        print(f"Error: Config file {path} does not exist.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_handler_dirs_from_config(config: dict) -> dict:
    """Return {handler_name: handler_dir_path} for all enabled handlers in a config."""
    base_dir = Path(DirectoryInfo.get_project_dir())
    handler_configs = config.get("default", {}).get("chat_engine", {}).get("handler_configs", {})
    result = {}
    for handler_name, cfg in handler_configs.items():
        if not cfg.get("enabled", True):
            continue
        module_val = cfg.get("module", "")
        if not module_val:
            continue
        module_path = Path(module_val).parent
        handler_dir = base_dir / "src" / "handlers" / module_path
        if handler_dir.exists():
            result[handler_name] = handler_dir
    return result


def get_all_handler_dirs() -> dict:
    """Return handler dirs for ALL handlers that have a pyproject.toml.

    Supports both single-level (e.g. src/handlers/agent/) and two-level
    (e.g. src/handlers/tts/cosyvoice/) directory layouts.
    """
    base_dir = Path(DirectoryInfo.get_project_dir())
    handler_base = base_dir / "src" / "handlers"
    result = {}
    for toml_path in handler_base.rglob("pyproject.toml"):
        parent = toml_path.parent
        rel = parent.relative_to(handler_base)
        depth = len(rel.parts)
        if depth in (1, 2):
            result[parent.name] = parent
    return result


def parse_pyproject_deps(pyproject_path: Path) -> list:
    """Parse dependencies from a handler's pyproject.toml, returning raw dep strings."""
    try:
        content = pyproject_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []

    in_deps = False
    deps = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("dependencies"):
            if "[" in stripped:
                in_deps = True
                continue
        if in_deps:
            if stripped == "]":
                break
            dep = stripped.strip('",').strip("',").strip()
            if dep and not dep.startswith("#"):
                deps.append(dep)
    return deps


def normalize_pkg_name(name: str) -> str:
    """Normalize package name: lowercase, replace hyphens/underscores/dots with hyphens."""
    return re.sub(r"[-_.]+", "-", name).lower()


def split_dep(dep_str: str) -> tuple:
    """Split 'package>=1.0' into ('package', '>=1.0'). Handles extras like pkg[extra]."""
    match = re.match(r"^([a-zA-Z0-9_\-\.]+(?:\[[^\]]+\])?)(.*)$", dep_str.strip())
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return dep_str.strip(), ""


def collect_and_merge_deps(handler_dirs: dict) -> list:
    """Collect deps from all handler pyproject.toml files and merge them.
    
    Returns a list of pip-installable requirement strings.
    """
    dep_map = {}

    for handler_name, handler_dir in handler_dirs.items():
        toml_path = handler_dir / "pyproject.toml"
        if not toml_path.exists():
            continue
        raw_deps = parse_pyproject_deps(toml_path)
        for dep_str in raw_deps:
            pkg_with_extra, version_spec = split_dep(dep_str)
            pkg_base = pkg_with_extra.split("[")[0]
            norm_name = normalize_pkg_name(pkg_base)

            if norm_name in {normalize_pkg_name(s) for s in MUSETALK_SPECIAL_PKGS}:
                continue

            # Skip packages managed by the root project (e.g. torch)
            if norm_name in {normalize_pkg_name(s) for s in PROTECTED_PACKAGES.keys()}:
                continue

            # Apply package name replacements (e.g. onnxruntime -> onnxruntime-gpu)
            replacement_norm = {normalize_pkg_name(k): v for k, v in PACKAGE_REPLACEMENTS.items()}
            if norm_name in replacement_norm:
                new_pkg = replacement_norm[norm_name]
                pkg_with_extra = new_pkg
                norm_name = normalize_pkg_name(new_pkg)
                dep_str = f"{new_pkg}{version_spec}"

            override_key = norm_name
            if override_key in {normalize_pkg_name(k) for k in VERSION_OVERRIDES}:
                for orig_key, override_ver in VERSION_OVERRIDES.items():
                    if normalize_pkg_name(orig_key) == override_key:
                        dep_map[norm_name] = f"{pkg_with_extra}{override_ver}"
                        break
            else:
                if norm_name not in dep_map:
                    dep_map[norm_name] = dep_str
    return list(dep_map.values())


def run_cmd(cmd: list, description: str = "", check: bool = True, dry_run: bool = False, env: dict = None):
    """Run a shell command with logging."""
    cmd_str = " ".join(cmd)
    if description:
        print(f"\n{'='*60}")
        print(f"  {description}")
        print(f"{'='*60}")
    print(f"$ {cmd_str}")

    if dry_run:
        print("  [dry-run] skipped")
        return

    result = subprocess.run(cmd, check=False, env=env)
    if check and result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        print(f"  Command: {cmd_str}")
        sys.exit(1)
    return result


def main():
    args = parse_args()

    if not is_venv_active():
        print("Error: Not running in a virtual environment.")
        print("Please run with: uv run install.py --config <config_file>")
        sys.exit(1)

    if not args.configs and not args.install_all:
        print("Error: Please specify --config <path> or --all")
        print("Examples:")
        print("  uv run install.py --config config/chat_with_lam.yaml")
        print("  uv run install.py --config config/a.yaml --config config/b.yaml")
        print("  uv run install.py --all")
        sys.exit(1)

    # Collect handler directories
    if args.install_all:
        print("Mode: Install ALL handler dependencies")
        handler_dirs = get_all_handler_dirs()
        configs = []
    else:
        print(f"Mode: Install dependencies for {len(args.configs)} config(s)")
        handler_dirs = {}
        configs = []
        for config_path in args.configs:
            print(f"  Loading: {config_path}")
            config = load_yaml(config_path)
            configs.append(config)
            handler_dirs.update(get_handler_dirs_from_config(config))

    if not handler_dirs:
        print("No handler directories found!")
        sys.exit(1)

    print(f"\nDiscovered {len(handler_dirs)} handler(s):")
    for name, path in sorted(handler_dirs.items()):
        print(f"  - {name}: {path}")

    # Collect and merge dependencies
    merged_deps = collect_and_merge_deps(handler_dirs)

    # Inject protected packages as version constraints so transitive
    # dependencies (e.g. xformers -> torch) cannot downgrade them.
    for pkg, ver in PROTECTED_PACKAGES.items():
        merged_deps.append(f"{pkg}{ver}")

    if not merged_deps:
        print("No dependencies to install.")
        return

    # Split into normal deps and no-build-isolation deps
    nbi_norm = {normalize_pkg_name(p) for p in NO_BUILD_ISOLATION_PKGS}
    nbi_deps = []
    normal_deps = []
    for dep in merged_deps:
        pkg_name, _ = split_dep(dep)
        pkg_base = pkg_name.split("[")[0]
        if normalize_pkg_name(pkg_base) in nbi_norm:
            nbi_deps.append(dep)
        else:
            normal_deps.append(dep)

    print(f"\nMerged {len(merged_deps)} unique dependencies:")
    for dep in sorted(merged_deps):
        print(f"  {dep}")
    if nbi_deps:
        print(f"\n  (no-build-isolation: {', '.join(nbi_deps)})")

    build_tools = ["setuptools>=69.5.1", "pip", "wheel"]

    # Phase 0: Always install build tools
    run_cmd(
        ["uv", "pip", "install"] + build_tools,
        description="Installing build tools (setuptools, pip, wheel)",
        dry_run=args.dry_run,
    )

    # Phase 1: Unified install of all normal handler dependencies
    # (installed before NBI packages so build tools like ninja are available)
    if normal_deps:
        run_cmd(
            ["uv", "pip", "install"] + normal_deps,
            description="Installing all handler dependencies (unified resolution)",
            dry_run=args.dry_run,
        )

    # Phase 2: Install no-build-isolation packages separately
    # (e.g. flash-attn needs ninja from Phase 1 and --no-build-isolation)
    # Limit parallel compilation jobs to avoid server OOM / crash.
    if nbi_deps:
        nbi_env = os.environ.copy()
        nbi_env["MAX_JOBS"] = str(MAX_COMPILE_JOBS)
        run_cmd(
            ["uv", "pip", "install", "--no-build-isolation"] + nbi_deps,
            description=f"Installing packages requiring no-build-isolation (MAX_JOBS={MAX_COMPILE_JOBS})",
            dry_run=args.dry_run,
            env=nbi_env,
        )

    # Phase 3: Install download tools (HuggingFace CLI for model downloads)
    # v0.x provides 'huggingface-cli', v1.x provides 'hf' (cli extra was removed in v1.0)
    run_cmd(
        ["uv", "pip", "install", "huggingface_hub"],
        description="Installing download tools (HuggingFace CLI)",
        dry_run=args.dry_run,
    )

    print(f"\n{'='*60}")
    print("  Installation completed successfully!")
    print(f"{'='*60}")
    if args.configs:
        for config_path in args.configs:
            print(f"  Run with: uv run src/demo.py --config {config_path}")
    else:
        print("  All handler dependencies installed. Run with any config.")


if __name__ == "__main__":
    main()
