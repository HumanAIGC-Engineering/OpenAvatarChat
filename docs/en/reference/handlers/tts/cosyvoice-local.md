# CosyVoice Local Inference Handler

> [!WARNING]
> On Windows, pynini compilation fails via PyPI. Use Conda to install the precompiled package.

## Windows Installation

```bash
conda create -n openavatarchat python=3.10
conda activate openavatarchat
conda install -c conda-forge pynini==2.1.6
set VIRTUAL_ENV=%CONDA_PREFIX%
uv run --active install.py --config config/chat_with_openai_compatible.yaml
uv run --active src/demo.py --config config/chat_with_openai_compatible.yaml
```
