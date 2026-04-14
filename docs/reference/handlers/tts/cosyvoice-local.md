# CosyVoice 本地推理 Handler

> [!WARNING]
> CosyVoice 依赖中的 pynini 包在 Windows 下通过 PyPI 获取时会出现编译参数不支持的问题。CosyVoice 官方建议在 Windows 下用 Conda 安装 conda-forge 中的 pynini 预编译包。

## Windows 安装步骤

1. 安装 Anaconda 或 [Miniconda](https://docs.anaconda.net.cn/miniconda/install/)
```bash
conda create -n openavatarchat python=3.10
conda activate openavatarchat
conda install -c conda-forge pynini==2.1.6
```

2. 设置 uv 环境变量
```bash
# cmd
set VIRTUAL_ENV=%CONDA_PREFIX%
# powershell
$env:VIRTUAL_ENV=$env:CONDA_PREFIX
```

3. 安装依赖和运行
```bash
uv run --active install.py --config config/chat_with_openai_compatible.yaml
uv run --active src/demo.py --config config/chat_with_openai_compatible.yaml
```

> [!Note]
> TTS 默认为 CosyVoice 的 `iic/CosyVoice-300M-SFT` + `中文女`，可以通过修改为其他模型配合 `ref_audio_path` 和 `ref_audio_text` 进行音色复刻。
