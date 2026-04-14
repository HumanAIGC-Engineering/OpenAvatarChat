#!/usr/bin/env python3
"""
Unified model download script for OpenAvatarChat.

A Python equivalent of the individual download scripts
(download_liteavatar_weights.sh, download_musetalk_weights.sh,
download_smart_turn_weights.sh), providing a unified, configurable interface.

Usage:
    uv run scripts/download_models.py --config config/xxx.yaml
    uv run scripts/download_models.py --all
    uv run scripts/download_models.py --handler liteavatar --handler musetalk
    uv run scripts/download_models.py --all --source huggingface
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent

HANDLER_MODEL_REGISTRY = {
    "liteavatar": {
        "label": "LiteAvatar weights",
        "description": "LiteAvatar neural network weights (lm.pb, model_1.onnx, model.pb)",
    },
    "lam": {
        "label": "LAM models",
        "description": "wav2vec2-base-960h + LAM_audio2exp_streaming",
    },
    "musetalk": {
        "label": "MuseTalk weights",
        "description": "MuseTalk, SD-VAE, Whisper, DWPose, SyncNet, Face-Parse, s3fd",
    },
    "smart_turn_eou": {
        "label": "Smart Turn VAD model",
        "description": "Smart Turn v3 ONNX model for end-of-utterance detection",
    },
    "flashhead": {
        "label": "FlashHead models",
        "description": "SoulX-FlashHead-1_3B (Lite/Pro) + wav2vec2-base-960h",
    },
}

MODULE_TO_HANDLER = {
    "avatar/liteavatar": "liteavatar",
    "avatar/lam": "lam",
    "avatar/musetalk": "musetalk",
    "vad/smart_turn_eou": "smart_turn_eou",
    "avatar/flashhead": "flashhead",
}


def run_cmd(cmd, description="", check=True, env=None):
    merged_env = {**os.environ, **(env or {})}
    if description:
        print(f"\n  [{description}]")
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, check=False, env=merged_env)
    if check and result.returncode != 0:
        print(f"  Warning: command exited with code {result.returncode}")
        return False
    return True


def ensure_package(pkg_name, pip_spec=None):
    """Ensure a Python package is installed, install it if missing."""
    try:
        __import__(pkg_name)
        return
    except ImportError:
        pass
    spec = pip_spec or pkg_name
    if shutil.which("uv") and (PROJECT_ROOT / ".venv").is_dir():
        run_cmd(["uv", "pip", "install", spec], f"Installing {spec}")
    else:
        run_cmd([sys.executable, "-m", "pip", "install", spec], f"Installing {spec}")


def _find_hf_cli():
    """Find the HuggingFace CLI command.

    huggingface_hub v0.x: 'huggingface-cli'
    huggingface_hub v1.x: 'hf' (huggingface-cli was removed in v1.0)
    """
    venv_bin = Path(sys.executable).parent
    for name in ("huggingface-cli", "hf"):
        if shutil.which(name):
            return name
        venv_path = venv_bin / name
        if venv_path.exists():
            return str(venv_path)
    return None


def _ensure_hf_cli():
    """Ensure HuggingFace CLI is available and return the command name."""
    cmd = _find_hf_cli()
    if cmd:
        return cmd
    spec = "huggingface_hub"
    if shutil.which("uv") and (PROJECT_ROOT / ".venv").is_dir():
        run_cmd(["uv", "pip", "install", spec], f"Installing {spec}")
    else:
        run_cmd([sys.executable, "-m", "pip", "install", spec], f"Installing {spec}")
    cmd = _find_hf_cli()
    if cmd:
        return cmd
    print("  Warning: HuggingFace CLI not found, falling back to python -m huggingface_hub")
    return None


def _local_files_present(local_dir, patterns=None):
    """Check if expected files already exist locally."""
    p = Path(local_dir)
    if not p.exists():
        return False
    if patterns:
        for pat in patterns:
            if not list(p.glob(pat)):
                return False
        return True
    non_meta = [f for f in p.rglob("*") if f.is_file()
                and ".huggingface" not in f.parts
                and ".modelscope" not in f.parts]
    return len(non_meta) > 0


def _hf_download(repo_id, local_dir, include=None, use_mirror=False):
    """Download from HuggingFace using the HuggingFace CLI.

    Supports both huggingface-cli (v0.x) and hf (v1.x).

    When use_mirror=True, sets HF_ENDPOINT=https://hf-mirror.com
    (same as download_musetalk_weights.sh / download_smart_turn_weights.sh).
    """
    cli = _ensure_hf_cli()
    Path(local_dir).mkdir(parents=True, exist_ok=True)
    if cli:
        cmd = [cli, "download", repo_id]
    else:
        cmd = [sys.executable, "-m", "huggingface_hub", "download", repo_id]
    if include:
        is_hf_v1 = cli and Path(cli).name == "hf"
        has_glob = any(c in f for f in include for c in "*?[")
        if is_hf_v1 and not has_glob:
            # v1.x: exact filenames as positional arguments
            cmd.extend(include)
        else:
            # v0.x or glob patterns: use --include flag
            cmd.extend(["--include"] + include)
    cmd.extend(["--local-dir", str(local_dir)])
    env = {"HF_ENDPOINT": "https://hf-mirror.com"} if use_mirror else None
    source_label = "hf-mirror.com" if use_mirror else "HuggingFace"
    ok = run_cmd(cmd, f"Downloading {repo_id} from {source_label}", env=env)
    if not ok:
        print(f"\n  *** 下载失败: {repo_id}")
        if use_mirror:
            print("  *** hf-mirror.com 也无法访问，请尝试:")
            print("  ***   1. 配置网络代理")
            print(f"  ***   2. 手动下载模型到 {local_dir}")
        else:
            print("  *** 如果无法访问 HuggingFace，请尝试:")
            print("  ***   1. 使用 --source modelscope 通过镜像下载")
            print("  ***   2. 配置网络代理")
            print(f"  ***   3. 手动下载模型到 {local_dir}")
    return ok


def get_handlers_from_config(config_path):
    """Parse a config YAML and return the set of handler keys needing models."""
    path = Path(config_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    if not path.exists():
        print(f"Error: config file not found: {path}")
        return set()
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    handler_configs = config.get("default", {}).get("chat_engine", {}).get("handler_configs", {})
    handlers = set()
    for _name, cfg in handler_configs.items():
        if not cfg.get("enabled", True):
            continue
        module_val = cfg.get("module", "")
        if not module_val:
            continue
        for prefix, handler_key in MODULE_TO_HANDLER.items():
            if module_val.startswith(prefix):
                handlers.add(handler_key)
                break
    return handlers


# ---------------------------------------------------------------------------
# Per-handler download implementations
# Each function replicates the logic from the corresponding shell script.
# ---------------------------------------------------------------------------

def download_liteavatar(source, **_kwargs):
    """Replicates scripts/download_liteavatar_weights.sh -> download_model.sh

    Always uses ModelScope (the only source defined by the project).
    """
    lite_dir = PROJECT_ROOT / "src" / "handlers" / "avatar" / "liteavatar" / "algo" / "liteavatar"
    weights_dir = lite_dir / "weights"
    if (weights_dir / "model_1.onnx").exists():
        print("  LiteAvatar weights already exist, skipping.")
        return True

    ensure_package("modelscope")
    run_cmd(
        ["modelscope", "download", "--model", "HumanAIGC-Engineering/LiteAvatarGallery",
         "lite_avatar_weights/lm.pb", "lite_avatar_weights/model_1.onnx",
         "lite_avatar_weights/model.pb", "--local_dir", str(lite_dir)],
        "Downloading LiteAvatar weights from ModelScope",
    )

    # Move files to expected locations (same as download_model.sh)
    src_dir = lite_dir / "lite_avatar_weights"
    if src_dir.exists():
        speech_dir = weights_dir / "speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
        lm_dir = speech_dir / "lm"
        for d in [weights_dir, speech_dir, lm_dir]:
            d.mkdir(parents=True, exist_ok=True)
        lm_src = src_dir / "lm.pb"
        onnx_src = src_dir / "model_1.onnx"
        pb_src = src_dir / "model.pb"
        if lm_src.exists():
            shutil.move(str(lm_src), str(lm_dir / "lm.pb"))
        if onnx_src.exists():
            shutil.move(str(onnx_src), str(weights_dir / "model_1.onnx"))
        if pb_src.exists():
            shutil.move(str(pb_src), str(speech_dir / "model.pb"))
        shutil.rmtree(str(src_dir), ignore_errors=True)
    return True


def download_lam(source, **_kwargs):
    """Download LAM models following README instructions.

    wav2vec2-base-960h: git clone from HuggingFace or ModelScope
    LAM_audio2exp: wget from HuggingFace or Aliyun OSS
    """
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    # wav2vec2-base-960h (README: git clone --depth 1)
    wav2vec_dir = models_dir / "wav2vec2-base-960h"
    if wav2vec_dir.exists():
        print("  wav2vec2-base-960h already exists, skipping.")
    else:
        if source == "huggingface":
            run_cmd(
                ["git", "clone", "--depth", "1",
                 "https://huggingface.co/facebook/wav2vec2-base-960h",
                 str(wav2vec_dir)],
                "Downloading wav2vec2-base-960h from HuggingFace",
            )
        else:
            run_cmd(
                ["git", "clone", "--depth", "1",
                 "https://www.modelscope.cn/AI-ModelScope/wav2vec2-base-960h.git",
                 str(wav2vec_dir)],
                "Downloading wav2vec2-base-960h from ModelScope",
            )

    # LAM_audio2exp (README: wget + tar)
    lam_dir = models_dir / "LAM_audio2exp"
    lam_dir.mkdir(exist_ok=True)
    tar_name = "LAM_audio2exp_streaming.tar"
    if (lam_dir / "pretrained_models").exists() or (lam_dir / "config.yaml").exists():
        print("  LAM_audio2exp already exists, skipping.")
    else:
        if source == "huggingface":
            url = f"https://huggingface.co/3DAIGC/LAM_audio2exp/resolve/main/{tar_name}"
            src_label = "HuggingFace"
        else:
            url = f"https://virutalbuy-public.oss-cn-hangzhou.aliyuncs.com/share/aigc3d/data/LAM/{tar_name}"
            src_label = "Aliyun OSS"
        tar_path = lam_dir / tar_name
        run_cmd(["wget", "-c", url, "-O", str(tar_path)],
                f"Downloading LAM_audio2exp from {src_label}")
        if tar_path.exists():
            run_cmd(["tar", "-xf", str(tar_path), "-C", str(lam_dir)],
                    "Extracting LAM_audio2exp")
            tar_path.unlink(missing_ok=True)
    return True


def download_musetalk(source, **_kwargs):
    """Replicates scripts/download_musetalk_weights.sh.

    Uses huggingface-cli download (fixing the shell script's `hf` command).
    s3fd always comes from ModelScope.
    """
    models_dir = PROJECT_ROOT / "models"
    mt_dir = models_dir / "musetalk"

    # Create directories (same as shell script)
    for d in [models_dir, mt_dir, mt_dir / "musetalkV15", mt_dir / "syncnet",
              mt_dir / "dwpose", mt_dir / "whisper",
              models_dir / "sd-vae", models_dir / "face-parse-bisent"]:
        d.mkdir(parents=True, exist_ok=True)

    # (repo_id, local_dir, hf_include, check_patterns)
    # hf_include: passed to huggingface-cli --include (None = download all)
    # check_patterns: glob patterns for local existence check
    downloads = [
        ("TMElyralab/MuseTalk", str(mt_dir),
         None, ["musetalkV15/unet.pth", "musetalkV15/musetalk.json"]),
        ("stabilityai/sd-vae-ft-mse", str(models_dir / "sd-vae"),
         None, ["diffusion_pytorch_model.*"]),
        ("openai/whisper-tiny", str(mt_dir / "whisper"),
         ["config.json", "pytorch_model.bin", "preprocessor_config.json"],
         ["config.json", "pytorch_model.bin", "preprocessor_config.json"]),
        ("yzd-v/DWPose", str(mt_dir / "dwpose"),
         ["dw-ll_ucoco_384.onnx"], ["dw-ll_ucoco_384.onnx"]),
        ("ByteDance/LatentSync", str(mt_dir / "syncnet"),
         ["latentsync_syncnet.pt"], ["latentsync_syncnet.pt"]),
        ("ManyOtherFunctions/face-parse-bisent", str(models_dir / "face-parse-bisent"),
         ["79999_iter.pth", "resnet18-5c106cde.pth"],
         ["79999_iter.pth", "resnet18-5c106cde.pth"]),
    ]

    use_mirror = (source == "modelscope")
    all_ok = True
    for repo_id, local_dir, hf_include, check_patterns in downloads:
        if _local_files_present(local_dir, check_patterns):
            print(f"\n  [Skipping {repo_id}] files already exist at {local_dir}")
            continue
        if not _hf_download(repo_id, local_dir, include=hf_include, use_mirror=use_mirror):
            all_ok = False

    # s3fd from ModelScope (same as shell script: git clone)
    s3fd_dir = mt_dir / "s3fd-619a316812"
    if s3fd_dir.exists():
        print("  s3fd already exists, skipping.")
    else:
        run_cmd(
            ["git", "clone", "https://www.modelscope.cn/HaveAnApplePie/s3fd-619a316812.git",
             str(s3fd_dir)],
            "Downloading s3fd from ModelScope",
        )

    # Create symlink for torch hub cache (replaces manual ln -s in README)
    cache_dir = Path.home() / ".cache" / "torch" / "hub" / "checkpoints"
    cache_dir.mkdir(parents=True, exist_ok=True)
    if s3fd_dir.exists():
        for ckpt in s3fd_dir.glob("*.pth"):
            target = cache_dir / ckpt.name
            if not target.exists():
                try:
                    target.symlink_to(ckpt.resolve())
                    print(f"  Symlinked {ckpt.name} -> {target}")
                except OSError:
                    shutil.copy2(str(ckpt), str(target))
                    print(f"  Copied {ckpt.name} -> {target}")
    return all_ok


def download_smart_turn(source, **_kwargs):
    """Replicates scripts/download_smart_turn_weights.sh.

    Uses huggingface-cli download (fixing the shell script's `hf` command).
    """
    model_dir = PROJECT_ROOT / "models" / "smart_turn"
    onnx_files = list(model_dir.glob("*.onnx")) if model_dir.exists() else []
    if onnx_files:
        print(f"  Smart Turn models already exist ({len(onnx_files)} ONNX file(s)), skipping.")
        return True

    model_dir.mkdir(parents=True, exist_ok=True)
    use_mirror = (source == "modelscope")
    ok = _hf_download("pipecat-ai/smart-turn-v3", str(model_dir), use_mirror=use_mirror)

    onnx_files = list(model_dir.glob("*.onnx"))
    if onnx_files:
        print(f"  Found {len(onnx_files)} ONNX file(s).")
    elif not ok:
        print("  Warning: No ONNX files found. Download may have failed.")
    return ok


def download_flashhead(source, **_kwargs):
    """Download FlashHead models.

    SoulX-FlashHead-1_3B: from HuggingFace (Soul-AILab/SoulX-FlashHead-1_3B)
    wav2vec2-base-960h: shared with LAM, from HuggingFace or ModelScope
    """
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    # wav2vec2-base-960h (shared with LAM handler)
    wav2vec_dir = models_dir / "wav2vec2-base-960h"
    if wav2vec_dir.exists():
        print("  wav2vec2-base-960h already exists, skipping.")
    else:
        if source == "huggingface":
            run_cmd(
                ["git", "clone", "--depth", "1",
                 "https://huggingface.co/facebook/wav2vec2-base-960h",
                 str(wav2vec_dir)],
                "Downloading wav2vec2-base-960h from HuggingFace",
            )
        else:
            run_cmd(
                ["git", "clone", "--depth", "1",
                 "https://www.modelscope.cn/AI-ModelScope/wav2vec2-base-960h.git",
                 str(wav2vec_dir)],
                "Downloading wav2vec2-base-960h from ModelScope",
            )

    # SoulX-FlashHead-1_3B
    flashhead_dir = models_dir / "SoulX-FlashHead-1_3B"
    if _local_files_present(flashhead_dir, ["Model_Lite/*"]):
        print("  SoulX-FlashHead-1_3B already exists, skipping.")
    else:
        use_mirror = (source == "modelscope")
        _hf_download(
            "Soul-AILab/SoulX-FlashHead-1_3B",
            str(flashhead_dir),
            use_mirror=use_mirror,
        )
    return True


DOWNLOAD_FUNCTIONS = {
    "liteavatar": download_liteavatar,
    "lam": download_lam,
    "musetalk": download_musetalk,
    "smart_turn_eou": download_smart_turn,
    "flashhead": download_flashhead,
}


def resolve_source(source, handler_key):
    """Resolve 'auto' source to a concrete source for a given handler.

    auto: liteavatar/lam use ModelScope, musetalk/smart_turn use HuggingFace official.
    modelscope: all handlers use ModelScope / hf-mirror.com.
    huggingface: all handlers use HuggingFace official.
    """
    if source != "auto":
        return source
    prefer_modelscope = {"liteavatar", "lam"}
    # flashhead uses HuggingFace as primary source
    return "modelscope" if handler_key in prefer_modelscope else "huggingface"


def main():
    parser = argparse.ArgumentParser(
        description="Unified model download tool for OpenAvatarChat. "
                    "Reads config YAML(s) or accepts explicit handler names to "
                    "download all required model files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  uv run scripts/download_models.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml\n"
            "  uv run scripts/download_models.py --all\n"
            "  uv run scripts/download_models.py --all --source huggingface\n"
            "  uv run scripts/download_models.py --handler liteavatar --handler musetalk\n"
        ),
    )
    parser.add_argument(
        "--config", type=str, action="append", dest="configs",
        help="Config YAML file (can be specified multiple times)",
    )
    parser.add_argument(
        "--all", action="store_true", dest="download_all",
        help="Download models for ALL handlers",
    )
    parser.add_argument(
        "--handler", type=str, action="append", dest="handlers",
        choices=list(HANDLER_MODEL_REGISTRY.keys()),
        help="Download models for specific handler(s)",
    )
    parser.add_argument(
        "--source", type=str, default="auto",
        choices=["auto", "huggingface", "modelscope"],
        help="Download source (default: auto = ModelScope for supported models, HuggingFace official for others; "
             "modelscope = all via ModelScope/hf-mirror; huggingface = all via HuggingFace official)",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all available handler model downloads",
    )
    args = parser.parse_args()

    if args.list:
        print("Available handler model downloads:\n")
        for key, info in HANDLER_MODEL_REGISTRY.items():
            print(f"  {key:20s} - {info['label']}")
            print(f"  {' ':20s}   {info['description']}")
        return

    needed = set()
    if args.download_all:
        needed = set(HANDLER_MODEL_REGISTRY.keys())
    elif args.handlers:
        needed = set(args.handlers)
    elif args.configs:
        for cfg_path in args.configs:
            needed |= get_handlers_from_config(cfg_path)
    else:
        parser.print_help()
        print("\nError: specify --config, --all, or --handler")
        sys.exit(1)

    if not needed:
        print("No handlers requiring model downloads found in the given config(s).")
        return

    print(f"Models to download ({len(needed)} handler(s)):")
    for key in sorted(needed):
        info = HANDLER_MODEL_REGISTRY.get(key, {})
        src = resolve_source(args.source, key)
        print(f"  - {info.get('label', key)} [{src}]")

    print()

    success = True
    for key in sorted(needed):
        info = HANDLER_MODEL_REGISTRY.get(key, {})
        func = DOWNLOAD_FUNCTIONS.get(key)
        if not func:
            print(f"  Skip: no download function for '{key}'")
            continue

        src = resolve_source(args.source, key)
        print(f"\n{'='*60}")
        print(f"  Downloading: {info.get('label', key)}")
        print(f"  Source: {src}")
        print(f"{'='*60}")
        try:
            ok = func(source=src)
            if not ok:
                success = False
        except Exception as e:
            print(f"  Error downloading {key}: {e}")
            success = False

    print(f"\n{'='*60}")
    if success:
        print("  All model downloads completed!")
    else:
        print("  Some downloads may have failed. Check the output above.")
        if args.source != "modelscope":
            print("  如果 HuggingFace 下载失败，可尝试: uv run scripts/download_models.py --all --source modelscope")
        else:
            print("  如果镜像下载也失败，请配置网络代理后重试")
    print(f"{'='*60}")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
