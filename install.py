import argparse
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from src.engine_utils.directory_info import DirectoryInfo


def is_venv_active():
    """Check if running inside a virtual environment"""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or (os.getenv('VIRTUAL_ENV') is not None)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config/chat_with_minicpm.yaml",
                        help="Path to config file")
    parser.add_argument("--uv", action="store_true",
                        help="Use uv pip compiler instead of standard pip")
    parser.add_argument("--skip-core", action="store_true",
                        help="Skip installation of core dependencies")
    return parser.parse_args()


def load_configs(in_args):
    base_dir = DirectoryInfo.get_project_dir()
    config_path = Path(in_args.config) if os.path.isabs(in_args.config) \
        else Path(base_dir) / in_args.config

    print(f"Loading config from {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_module_files(config, use_uv=False):
    """Collect dependency files for enabled modules"""
    base_dir = Path(DirectoryInfo.get_project_dir())
    handler_configs = config.get("default", {}).get("chat_engine", {}).get("handler_configs", {})

    module_files = {}
    for handler_name, cfg in handler_configs.items():
        if not cfg.get("enabled", True):
            continue

        module_path = Path(cfg.get("module", "")).parent
        handler_dir = base_dir / "src/handlers" / module_path

        # Prefer pyproject.toml when using uv
        if use_uv:
            toml_file = handler_dir / "pyproject.toml"
            if toml_file.exists():
                module_files[handler_name] = toml_file
                continue

        # Fallback to requirements.txt
        req_file = handler_dir / "requirements.txt"
        if req_file.exists():
            module_files[handler_name] = req_file

    return module_files


def collect_root_file(use_uv=False):
    """Get root dependency file based on tool preference"""
    base_dir = Path(DirectoryInfo.get_project_dir())

    if use_uv:
        root_toml = base_dir / "pyproject.toml"
        if root_toml.exists():
            return root_toml

    root_req = base_dir / "requirements.txt"
    return root_req if root_req.exists() else None


def install_files(file_paths, use_uv=False):
    """Install dependencies from collected files"""
    try:
        for dep_file in file_paths:
            print(f"Installing from {dep_file}")

            if use_uv:
                cmd = ["uv", "pip", "install", "-r", str(dep_file)]
            else:
                cmd = [sys.executable, "-m", "pip", "install", "-r", str(dep_file)]

            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check virtual environment first
    if not is_venv_active():
        print("Error: Not running in a virtual environment.")
        print("Create and activate a venv first.")
        sys.exit(1)

    args = parse_args()
    config = load_configs(args)

    # Collect dependency files
    root_file = collect_root_file(args.uv)
    module_files = get_module_files(config, args.uv)

    # Prepare installation list
    install_paths = []
    if root_file and not args.skip_core:
        install_paths.append(root_file)
    install_paths.extend(module_files.values())

    if not install_paths:
        print("No dependency files found!")
        sys.exit(1)

    # Perform installation
    install_files(install_paths, args.uv)
    print("Dependencies installed successfully")
