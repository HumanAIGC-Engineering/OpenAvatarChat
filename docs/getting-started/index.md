# 快速开始

## 前置准备

> [!IMPORTANT]
> 本项目子模块以及依赖模型都需要使用 git lfs 模块，请确认 lfs 功能已安装
> ```bash
> sudo apt install git-lfs
> git lfs install 
> ```
> 本项目通过 git 子模块方式引用三方库，运行前需要更新子模块
> ```bash
> git submodule update --init --recursive --depth 1
> ```
> 本项目的运行依赖 CUDA，请确保本机 NVIDIA 驱动程序支持的 CUDA 版本 >= 12.8

## uv 安装

推荐安装 [uv](https://docs.astral.sh/uv/)，使用 uv 进行本地环境管理。

> 官方独立安装程序
> ```bash
> # On Windows.
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> # On macOS and Linux.
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> PyPI 安装
> ```bash
> # With pip.
> pip install uv
> # Or pipx.
> pipx install uv
> ```

## 依赖安装

`install.py` 是一站式依赖安装器，会自动解析配置文件、收集所有 handler 依赖、处理版本冲突，并完成特殊依赖的编译安装。

```bash
# 按配置安装依赖
uv run install.py --config <配置文件路径>.yaml

# 安装多个配置的依赖
uv run install.py --config config/a.yaml --config config/b.yaml

# 安装全部 handler 依赖
uv run install.py --all
```

> [!Note]
> `install.py` 会自动处理以下事项，无需手动执行额外脚本：
> - 安装构建工具（setuptools, pip, wheel）
> - 统一解析并合并所有 handler 的依赖，自动解决已知版本冲突
> - 需要编译安装的包（如 `flash-attn`）会自动使用 `--no-build-isolation` 并限制并行编译线程数

## 模型下载

部分 Handler 需要额外下载模型文件才能运行。推荐使用统一下载脚本：

```bash
# 按配置下载所需模型（自动选择下载源）
uv run scripts/download_models.py --config <配置文件路径>.yaml

# 下载所有 handler 的模型
uv run scripts/download_models.py --all

# 国内用户推荐指定 ModelScope 源
uv run scripts/download_models.py --config <配置文件路径>.yaml --source modelscope

# 海外用户可指定 HuggingFace 源
uv run scripts/download_models.py --config <配置文件路径>.yaml --source huggingface
```

> [!Note]
> - 默认模式 (`--source auto`) 会对有 ModelScope 源的模型优先使用 ModelScope
> - **国内用户推荐使用 `--source modelscope`**，该模式下 HuggingFace 源的模型会通过 hf-mirror.com 镜像下载
> - 所有下载脚本都需要在**项目根目录**下执行

## 运行

```bash
uv run src/demo.py --config <配置文件路径>.yaml
```
