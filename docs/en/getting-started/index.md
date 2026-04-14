# Getting Started

## Prerequisites

> [!IMPORTANT]
> This project requires git LFS for submodules and model dependencies:
> ```bash
> sudo apt install git-lfs
> git lfs install
> ```
> Update submodules before running:
> ```bash
> git submodule update --init --recursive --depth 1
> ```
> This project requires CUDA. Ensure NVIDIA driver supports CUDA >= 12.8.

## UV Installation

We recommend [uv](https://docs.astral.sh/uv/) for local environment management.

> Official standalone installer
> ```bash
> # On Windows.
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> # On macOS and Linux.
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> PyPI installation
> ```bash
> pip install uv
> ```

## Dependency Installation

`install.py` is a one-stop dependency installer that parses config YAML files, collects all handler dependencies, and resolves version conflicts.

```bash
# Install for a specific config
uv run install.py --config <path-to-config>.yaml

# Install for multiple configs
uv run install.py --config config/a.yaml --config config/b.yaml

# Install ALL handler dependencies
uv run install.py --all
```

## Model Download

```bash
# Download models for a specific config
uv run scripts/download_models.py --config <path-to-config>.yaml

# Download all handler models
uv run scripts/download_models.py --all

# Chinese users: specify ModelScope source
uv run scripts/download_models.py --config <path-to-config>.yaml --source modelscope

# Overseas users: specify HuggingFace source
uv run scripts/download_models.py --config <path-to-config>.yaml --source huggingface
```

## Run

```bash
uv run src/demo.py --config <path-to-config>.yaml
```
