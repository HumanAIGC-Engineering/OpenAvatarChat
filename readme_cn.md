<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<p align="center">
<strong><a href="README.md">English</a> | 中文</strong>
</p>


<p align="center">
<strong>模块化的交互数字人对话实现，能够在单台PC上运行完整功能。</strong>
</p>


<p align="center" style="display: flex; flex-direction: row; justify-content: center">
 🤗 <a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp<img alt="Static Badge" style="height: 10px;" src="./assets/images/modelscope_logo.png"> <a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp💬 <a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat/blob/main/assets/images/community_wechat.png">WeChat (微信)</a>
</p>

## 🔥核心亮点
- **低延迟数字人实时对话：平均回答延迟在2.2秒左右。**
- **多模态语言模型：支持多模态语言模型，包括文本、音频、视频等。**
- **模块化设计：使用模块化的设计，可以灵活地替换组件，实现不同功能组合。**


## 📢 最新动态

### 更新日志
- [2025.04.18] ⭐️⭐️⭐️ 版本 0.3.0发布:
  - 增加对LAM数字人 (能够单图秒级打造超写实3D数字人的开源项目) 的支持
  - 增加使用百炼API的tts handler，可以大幅减少对GPU的依赖
  - 增加对微软Edge TTS的支持
  - 现在使用uv进行python的包管理，依赖可以按照配置中所激活的handler进行安装
  - CSS响应式布局更新
- [2025.04.14] ⭐️⭐️⭐️ 版本 0.2.2发布：
  - 100个新形象发布，请见[LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)
  - 默认使用GPU后端运行数字人
- [2025.04.07] ⭐️⭐️⭐️ 版本 0.2.1发布： 
  - 增加历史记录支持 
  - 支持文本输入 
  - 启动时不再强制要求摄像头存在 
  - 优化模块化加载方式
- [2025.02.20] ⭐️⭐️⭐️ 版本 0.1.0发布： 
  - 模块化的实时交互对话数字人 
  - 支持MiniCPM-o作为多模态语言模型和云端的 api 两种调用方

### 待办清单

- [x] 预置的数字人模型达到100个
- [x] 接入[LAM](https://github.com/aigc3d/LAM)：能够单图秒级打造超写实3D数字人的开源项目
- [ ] 接入[Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)

## Demo

我们部署在
<a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
    <img alt="Static Badge" style="height: 10px; margin-right: 1px;" src="./assets/images/modelscope_logo.png">
ModelScope
 </a>
和
<a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
    🤗
HuggingFace
 </a>
上均部署了一个体验服务，音频部分采用SenseVoice + Qwen-VL + CosyVoice实现，欢迎体验。

LiteAvatar
<div align="center">
  <video controls src="https://github.com/user-attachments/assets/e2861200-84b0-4c7a-93f0-f46268a0878b">
  </video>
</div>






## 📖目录 <!-- omit in toc -->

- [概览](#概览)
  - [简介](#简介)
  - [系统需求](#系统需求)
  - [性能指标](#性能指标)
  - [组件依赖](#组件依赖)
  - [预置模式](#预置模式)
- [快速开始](#安装部署)
  - [本地运行](#本地运行)
    - [uv安装](#uv安装)
    - [依赖安装](#依赖安装)
    - [运行](#运行)
  - [Docker运行](#dokcer运行)
- [相关模块安装方法](#相关模块安装方法)
  - [MiniCPM-o模块](#minicpm-o模块)
  - [CosyVoice模块](#cosyvoice模块)
  - [ASR + LLM + TTS API替换](#asr--llm--tts-api替换)
- [相关部署需求](#相关部署需求)
  - [准备ssl证书](#准备ssl证书)
  - [TURN Server](#turn-server)
- [配置说明](#配置说明)
  
  

## 概览

### 简介

Open Avatar Chat 是一个模块化的交互数字人对话实现，能够在单台PC上运行完整功能。目前支持MiniCPM-o作为多模态语言模型或者使用云端的 api 替换实现常规的ASR + LLM + TTS。这两种模式的结构如下图所示。更多的预置模式详见[下方](#预置模式)。

<p align="center">
<img src="./assets/images/data_flow.svg" />
</p>

### 系统需求
* Python版本 >=3.10, <3.12
* 支持CUDA的GPU
* 未量化的多模态语言模型MiniCPM-o需要20GB以上的显存。
* 数字人部分可以使用GPU/CPU进行推理，测试设备CPU为i9-13980HX，CPU推理下可以达到30FPS.

> [!TIP]
> 
> 使用int4量化版本的语言模型可以在不到10GB现存的显卡上运行，但可能会因为量化而影响效果。
> 
> 使用云端的 api 替换MiniCPM-o实现常规的ASR + LLM + TTS，可以大大减低配置需求，具体可参考 [ASR + LLM + TTS方式](#chat_with_openai_compatible_bailian_cosyvoiceyaml)


### 性能指标
在我们的测试中，使用配备 i9-13900KF 处理器和 Nvidia RTX 4090 显卡的 PC，我们记录了回答的延迟时间。经过十次测试，平均延迟约为 2.2 秒。延迟时间是从用户语音结束到数字人开始语音的时间间隔，其中包含了 RTC 双向数据传输时间、VAD（语音活动检测）停止延迟以及整个流程的计算时间。

### 组件依赖

| 类型       | 开源项目                                |Github地址|模型地址|
|----------|-------------------------------------|---|---|
| RTC      | HumanAIGC-Engineering/gradio-webrtc |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
| VAD      | snakers4/silero-vad                 |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad)||
| LLM      | OpenBMB/MiniCPM-o                   |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)| [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) |
| LLM-int4 | OpenBMB/MiniCPM-o                   |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)|[🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)|
| Avatar   | HumanAIGC/lite-avatar               |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar)||
| TTS      | FunAudioLLM/CosyVoice               |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/FunAudioLLM/CosyVoice)||
|Avatar|aigc3d/LAM_Audio2Expression|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/aigc3d/LAM_Audio2Expression)|[🤗](https://huggingface.co/3DAIGC/LAM_audio2exp)|
||facebook/wav2vec2-base-960h||[🤗](https://huggingface.co/facebook/wav2vec2-base-960h)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)|

### 预置模式

| CONFIG名称                                           | ASR |    LLM    |    TTS    | AVATAR|
|----------------------------------------------------|-----|:---------:|:---------:|------------|
| chat_with_gs.yaml                                  |SenseVoice|    API    |API| LAM        |
| chat_with_minicpm.yaml                             |MiniCPM-o| MiniCPM-o | MiniCPM-o | lite-avatar |
| chat_with_openai_compatible.yaml                   |SenseVoice|API|CosyVoice| lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice.yaml |SenseVoice|API|API| lite-avatar |
| chat_with_openai_compatible_edge_tts.yaml          |SenseVoice|API|edgetts| lite-avatar |


## 🚀安装部署

安装部署对应的模式前请先查看该模式使用到的**相关模块的安装方法**和[相关部署需求](#相关部署需求)。

### 选择配置
OpenAvatarChat按照配置文件启动并组织各个模块，可以按照选择的配置现在依赖的模型以及需要准备的ApiKey。项目在config目录下，提供以下预置的配置文件供参考：

#### chat_with_gs.yaml
使用[LAM](https://github.com/aigc3d/LAM)项目生成的gaussion splatting资产进行端侧渲染，语音使用百炼上的Cosyvoice，只有vad和asr运行在本地gpu，对机器性能依赖很轻，可以支持一机多路。
##### 使用的Handler
|类别|Handler|安装说明|
|---|---|---|
|Client|client/h5_rendering_client/cllient_handler_lam| [LAM端侧渲染 Client Handler](#lam端侧渲染-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI兼容API的语言模型Handler](#openai兼容api的语言模型handler)
|TTS|tts/bailian_tts/tts_handler_cosyvoice_bailian|[百炼 CosyVoice Handler](#百炼-cosyvoice-handler)|
|Avatar|avatar/lam/avatar_handler_lam_audio2expression|[LAM数字人驱动Handler](#lam数字人驱动handler)|
||||

#### chat_with_minicpm.yaml
使用minicpm进行本地的语音到语音的对话生成，对GPU的性能与显存大小有一定要求。
##### 使用的Handler
|类别|Handler|安装说明|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[服务端渲染 RTC Client Handler](#服务端渲染-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|LLM|llm/minicpm/llm_handler_minicpm|[MiniCPM多模态语言模型Handler](#minicpm多模态语言模型handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar数字人Handler](#liteavatar数字人handler)|
|||| 

#### chat_with_openai_compatible.yaml
该配置使用云端语言模型API，TTS使用cosyvoice，运行在本地。
#### 使用的Handler
|类别|Handler|安装说明|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[服务端渲染 RTC Client Handler](#服务端渲染-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI兼容API的语言模型Handler](#openai兼容api的语言模型handler)
|TTS|tts/cosyvoice/tts_handler_cosyvoice|[CosyVoice本地推理Handler](#cosyvoice本地推理handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar数字人Handler](#liteavatar数字人handler)|
||||

#### chat_with_openai_compatible_bailian_cosyvoice.yaml
语言模型与TTS都使用云端API，2D数字人下对设备要求较低的配置。
#### 使用的Handler
|类别|Handler|安装说明|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[服务端渲染 RTC Client Handler](#服务端渲染-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI兼容API的语言模型Handler](#openai兼容api的语言模型handler)
|TTS|tts/bailian_tts/tts_handler_cosyvoice_bailian|[百炼 CosyVoice Handler](#百炼-cosyvoice-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar数字人Handler](#liteavatar数字人handler)|
||||

#### chat_with_openai_compatible_edge_tts.yaml
该配置使用edge tts，效果稍差，但不需要百炼的API Key。
#### 使用的Handler
|类别|Handler|安装说明|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[服务端渲染 RTC Client Handler](#服务端渲染-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI兼容API的语言模型Handler](#openai兼容api的语言模型handler)
|TTS|tts/edgetts/tts_handler_edgetts|[Edge TTS Handler](#edge-tts-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar数字人Handler](#liteavatar数字人handler)|
||||


### 本地运行


> [!IMPORTANT]
> 本项目子模块以及依赖模型都需要使用git lfs模块，请确认lfs功能已安装
> ```bash
> sudo apt install git-lfs
> git lfs install 
> ```
> 本项目通过git子模块方式引用三方库，运行前需要更新子模块
> ```bash
> git submodule update --init --recursive
> ```
> 强烈建议：国内用户依然使用git clone的方式下载，而不要直接下载zip文件，方便这里的git submodule和git lfs的操作，github访问的问题，可以参考[github访问问题](https://github.com/maxiaof/github-hosts)
> 
> 如果遇到问题欢迎提 [issue](https://github.com/HumanAIGC-Engineering/OpenAvatarChat/issues) 给我们

#### uv安装

推荐安装[uv](https://docs.astral.sh/uv/)，使用uv进行进行本地环境管理。

> 官方独立安装程序
> ```bash
> # On Windows.
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> # On macOS and Linux.
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> PyPI安装
> ```
> # With pip.
> pip install uv
> # Or pipx.
> pipx install uv
> ```

#### 依赖安装

##### 安装全部依赖
```bash
uv sync --all-packages
```

##### 仅安装所需模式的依赖
```bash
uv run install.py --uv --config <配置文件的绝对路径>.yaml 
```

#### 运行
```bash
uv run src/demo.py --config <配置文件的绝对路径>.yaml
```


### Docker运行
容器化运行：容器依赖nvidia的容器环境，在准备好支持GPU的docker环境后，运行以下命令即可完成镜像的构建与启动：
```bash
./build_and_run.sh --config <配置文件的绝对路径>.yaml
```


## Handler依赖安装说明
### 服务端渲染 RTC Client Handler
暂无特别依赖和需要配置的内容。

### LAM端侧渲染 Client Handler
端侧渲染基于[服务端渲染 RTC Client Handler](#服务端渲染-rtc-client-handler)扩展，支持多路链接，可以通过配置文件选择形象。
#### 形象选择
形象可以通过LAM项目进行训练（LAM对话数字人资产生产流程待完善，敬请期待），本项目中预置了4个范例形象，位于src/handlers/client/h5_rendering_client/lam_samples下。用户可以通过在配置文件中用asset_path字段进行选择，也可以选择自行训练的资产文件。参考配置如下：
```yaml
LamClient:
  module: client/h5_rendering_client/client_handler_lam
  asset_path: "lam_samples/barbara.zip"
  concurrent_limit: 5
```
### OpenAI兼容API的语言模型Handler
本地推理的语言模型要求相对较高，如果你已有一个可调用的 LLM api_key,可以用这种方式启动来体验对话数字人。
可以通过配置文件选择所使用模型、系统prompt、API和API Key。参考配置如下，其中apikey可以被环境变量覆盖。
```yaml
LLM_Bailian: 
  moedl_name: "qwen-plus"
  system_prompt: "你是个AI对话数字人，你要用简短的对话来回答我的问题，并在合理的地方插入标点符号"
  api_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```
> [!TIP]
> 系统默认会获取项目当前目录下的.env文件用来获取环境变量。

> [!Note]
> * 代码内部调用方式
> ```python
> client = OpenAI(
>       api_key= self.api_key, 
>       base_url=self.api_url,
>   )
> completion = client.chat.completions.create(
>     model=self.model_name,
>     messages=[
>        self.system_prompt,
>         {'role': 'user', 'content': chat_text}
>     ],
>     stream=True
>     )
> ```
> * LLM默认为百炼api_url + api_key

### MiniCPM多模态语言模型Handler
#### 依赖模型
* MiniCPM-o-2.6
本项目可以使用MiniCPM-o-2.6作为多模态语言模型为数字人提供对话能力，用户可以按需从[Huggingface](https://huggingface.co/openbmb/MiniCPM-o-2_6)或者[Modelscope](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6)下载相关模型。建议将模型直接下载到 \<ProjectRoot\>/models/ 默认配置的模型路径指向这里，如果放置与其他位置，需要修改配置文件。scripts目录中有对应模型的下载脚本，可供在linux环境下使用，请在项目根目录下运行脚本：
```bash
scripts/download_MiniCPM-o_2.6.sh
```
```bash
scripts/download_MiniCPM-o_2.6-int4.sh
```

> [!NOTE]
> 本项目支持MiniCPM-o-2.6的原始模型以及int4量化版本，但量化版本需要安装专用分支的AutoGPTQ，相关细节请参考官方的[说明](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)

### 百炼 CosyVoice Handler
可以使用百炼提供CosyVoice API调用TTS能力，比本地推理对系统性能要求低，但需要在百炼上开通对应的能力。
参考配置如下：
```
CosyVoice:
  module: tts/bailian_tts/tts_handler_cosyvoice_bailian
  voice: "longxiaocheng"
  model_name: "cosyvoice-v1"
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```
同[OpenAI兼容API的语言模型Handler]一样，可以将api_key设置在配置中或通过环境变量来覆盖。
> [!TIP]
> 系统默认会获取项目当前目录下的.env文件用来获取环境变量。

### CosyVoice本地推理Handler

> [!WARNING]
> 因为CosyVoice依赖中的pynini包通过PyPI获取时在Windows下编译会出现编译参数不支持的问题。CosyVoice官方目前建议的解决方法是在Windows下用Conda安装
conda-forge中的pynini预编译包。

在Windows下如果使用本地的CosyVoice作为TTS的话，需要结合Conda和UV进行安装。具体依赖安装和运行流程如下：

1. 安装Anaconda或者[Miniconda](https://docs.anaconda.net.cn/miniconda/install/)
```bash
conda create -n openavatarchat python=3.10
conda activate openavatarchat
conda install -c conda-forge pynini==2.1.6
```

2. 设置uv要索引的环境变量为Conda环境
```bash
# cmd
set VIRTUAL_ENV=%CONDA_PREFIX%
# powershell 
$env:VIRTUAL_ENV=$env:CONDA_PREFIX
```

3. 在uv安装依赖和运行时，参数中添加--active，优先使用已激活的虚拟环境
```bash
# 安装依赖
uv sync --active --all-packages
# 仅安装所需依赖
uv run --active install.py --uv --config config/chat_with_openai_compatible.yaml
# 运行cosyvoice 
uv run --active src/demo.py --config config/chat_with_openai_compatible.yaml
```
> [!Note]
> TTS默认为CosyVoice的 `iic/CosyVoice-300M-SFT` + `中文女`，可以通过修改为`其他模型`配合 `ref_audio_path` 和 `ref_audio_text` 进行音色复刻

### Edge TTS Handler
集成微软的edge-tts，使用云端推理，无需申请api key，参考配置如下：
```yaml
Edge_TTS:
  module: tts/edgetts/tts_handler_edgetts
  voice: "zh-CN-XiaoxiaoNeural"
```

### LiteAvatar数字人Handler
集成LiteAvatar算法生产2D数字人对话，目前在modelscope的项目LiteAvatarGallery中提供了100个数字人形象可供使用，详情见[LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)。
LiteAvatar可以运行在CPU或GPU上，如果其他handler都没有对GPU的大开销，建议使用GPU进行推理。
参考配置如下：
```yaml
LiteAvatar:
  module: avatar/liteavatar/avatar_handler_liteavatar
  avatar_name: 20250408/sample_data
  fps: 25
  use_gpu: true
```

### LAM数字人驱动Handler
#### 依赖模型
* facebook/wav2vec2-base-960h [🤗](https://huggingface.co/facebook/wav2vec2-base-960h) [<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)
  * 从huggingface下载, 确保lfs已安装，使当前路径位于项目根目录，执行：
  ```
  git clone --depth 1 https://huggingface.co/facebook/wav2vec2-base-960h ./models/wav2vec2-base-960h
  ```
  * 从modelscope下载, 确保lfs已安装，使当前路径位于项目根目录，执行：
  ```
  git clone --depth 1 https://www.modelscope.cn/AI-ModelScope/wav2vec2-base-960h.git ./models/wav2vec2-base-960h
  ```
* LAM_audio2exp [🤗](https://huggingface.co/3DAIGC/LAM_audio2exp)
  * 从huggingface下载, 确保lfs已安装，使当前路径位于项目根目录，执行：
  ```
  git clone --depth 1 https://huggingface.co/3DAIGC/LAM_audio2exp ./models/LAM_audio2exp
  ```
  * 国内用户可以从oss地址下载, 使当前路径位于项目根目录，执行：
  ```
  wget https://virutalbuy-public.oss-cn-hangzhou.aliyuncs.com/share/aigc3d/data/LAM/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
  ```

## 相关部署需求
### 准备ssl证书
由于本项目使用rtc作为视音频传输的通道，用户如果需要从localhost以外的地方连接服务的话，需要准备ssl证书以开启https，默认配置会读取ssl_certs目录下的localhost.crt和localhost.key，用户可以相应修改配置来使用自己的证书。我们也在scripts目录下提供了生成自签名证书的脚本。需要在项目根目录下运行脚本以使生成的证书被放到默认位置。
```bash
scripts/create_ssl_certs.sh
```

### TURN Server
如果点击开始对话后，出现一直等待中的情况，可能你的部署环境存在NAT穿透方面的问题（如部署在云上机器等），需要进行数据中继。在Linux环境下，可以使用coturn来架设TURN服务。可参考以下操作在同一机器上安装、启动并配置使用coturn：
* 运行安装脚本
```console
$ chmod 777 scripts/setup_coturn.sh
# scripts/setup_coturn.sh
```
* 修改config配置文件，添加以下配置后启动服务
```yaml
default:
  service:
    rtc_config:
      # 使用turnserver时，使用以下配置
      urls: ["turn:your-turn-server.com:3478", "turns:your-turn-server.com:5349"]
      username: "your-username"
      credential: "your-credential"
```
* 确保防火墙（包括云上机器安全组等策略）开放coturn所需端口

### 配置说明
程序默认启动时，会读取 **<project_root>/configs/chat_with_minicpm.yaml** 中的配置，用户也可以在启动命令后加上--config参数来选择从其他配置文件启动。
```bash
uv run src/demo.py --config <配置文件的绝对路径>.yaml
```

可配置的参数列表：

|参数|默认值|说明|
|---|---|---|
|log.log_level|INFO|程序的日志级别。|
|service.host|0.0.0.0|Gradio服务的监听地址。|
|service.port|8282|Gradio服务的监听端口。|
|service.cert_file|ssl_certs/localhost.crt|SSL证书中的证书文件，如果cert_file和cert_key指向的文件都能正确读取，服务将会使用https。|
|service.cert_key|ssl_certs/localhost.key|SSL证书中的证书文件，如果cert_file和cert_key指向的文件都能正确读取，服务将会使用https。|
|chat_engine.model_root|models|模型的根目录。|
|chat_engine.handler_configs|N/A|由各Handler提供的可配置项。|

目前已实现的Handler提供如下的可配置参数：
* VAD

|参数|默认值|说明|
|---|---|---|
|SileraVad.speaking_threshold|0.5|判定输入音频为语音的阈值。|
|SileraVad.start_delay|2048|当模型输出概率持续大于阈值超过这个时间后，将起始超过阈值的时刻认定为说话的开始。以音频采样数为单位。|
|SileraVad.end_delay|2048|当模型输出的概率持续小于阈值超过这个时间后，判定说话内容结束。以音频采样数为单位。|
|SileraVad.buffer_look_back|1024|当使用较高阈值时，语音的起始部分往往有所残缺，该配置在语音的起始点往前回溯一小段时间，避免丢失语音，以音频采样数为单位。|
|SileraVad.speech_padding|512|返回的音频会在起始与结束两端加上这个长度的静音音频，已采样数为单位。|

* 语言模型

| 参数                             | 默认值           | 说明                                                                                 |
|--------------------------------|---------------|------------------------------------------------------------------------------------|
| S2S_MiniCPM.model_name         | MiniCPM-o-2_6 | 该参数用于选择使用的语言模型，可选"MiniCPM-o-2_6" 或者 "MiniCPM-o-2_6-int4"，需要确保model目录下实际模型的目录名与此一致。 |
| S2S_MiniCPM.voice_prompt       |               | MiniCPM-o的voice prompt                                                             |
| S2S_MiniCPM.assistant_prompt   |               | MiniCPM-o的assistant prompt                                                         |
| S2S_MiniCPM.enable_video_input | False         | 设置是否开启视频输入，**开启视频输入时，显存占用会明显增加，非量化模型再24G显存下可能会oom**                                |
| S2S_MiniCPM.skip_video_frame   | -1            | 控制开启视频输入时，输入视频帧的频率。-1表示仅每秒输入最后的一帧，0表示输入所有帧，大于0的值表示每一帧后会有这个数量的图像帧被跳过。               |

* ASR funasr模型

|参数|默认值|说明|
|---|---|---|
|ASR_Funasr.model_name|iic/SenseVoiceSmall|该参数用于选择funasr 下的[模型](https://github.com/modelscope/FunASR)，会自动下载模型，若需使用本地模型需改为绝对路径|

* LLM纯文本模型

|参数|默认值|说明|
|---|---|---|
|LLM_Bailian.model_name|qwen-plus|测试环境使用的百炼api,免费额度可以从[百炼](https://bailian.console.aliyun.com/#/home)获取|
|LLM_Bailian.system_prompt||默认系统prompt|
|LLM_Bailian.api_url||模型api_url|
|LLM_Bailian.api_key||模型api_key|

* TTS CosyVoice模型

|参数|默认值|说明|
|---|---|---|
|TTS_CosyVoice.api_url||自己利用其他机器部署cosyvocie server时需填|
|TTS_CosyVoice.model_name||可参考[CosyVoice](https://github.com/FunAudioLLM/CosyVoice)|
|TTS_CosyVoice.spk_id|中文女|使用官方sft 比如'中文女'|'中文男'，和ref_audio_path互斥|
|TTS_CosyVoice.ref_audio_path||参考音频的绝对路径，和spk_id 互斥，记得更换可参考音色的模型|
|TTS_CosyVoice.ref_audio_text||参考音频的文本内容|
|TTS_CosyVoice.sample_rate|24000|输出音频采样率|

* LiteAvatar数字人

|参数|默认值|说明|
|---|---|---|
|LiteAvatar.avatar_name|sample_data|数字人数据名，目前在modelscope的项目LiteAvatarGallery中提供了100个数字人形象可供使用，详情见[LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)。|
|LiteAvatar.fps|25|数字人的运行帧率，在性能较好的CPU上，可以设置为30FPS|
|LiteAvatar.enable_fast_mode|False|低延迟模式，打开后可以减低回答的延迟，但在性能不足的情况下，可能会在回答的开始产生语音卡顿。|
|LiteAvatar.use_gpu|True|LiteAvatar算法是否使用GPU，目前使用CUDA后端|

> [!IMPORTANT]
> 所有配置中的路径参数都可以使用绝对路径，或者相对于项目根目录的相对路径。

## 社区感谢

- 感谢社区同学“titan909”在B站上发布的[部署教程视频](https://www.bilibili.com/video/BV1FNZ8YNEA8)
- 感谢另一位社区同学“十字鱼”在B站上发布的一键安装包视频，并提供了下载（解压码在视频简介里面有,仔细找找）[一键包](https://www.bilibili.com/video/BV1V1oLYmEu3/?vd_source=29463f5b63a3510553325ba70f325293)


## Star历史
![](https://api.star-history.com/svg?repos=HumanAIGC-Engineering/OpenAvatarChat&type=Date)

## 引用

如果您在您的研究/项目中感到 OpenAvatarChat 为您提供了帮助，期待您能给一个 Star⭐和引用✏️

```
@software{avatarchat2025,
  author = {Gang Cheng, Tao Chen, Feng Wang, Binchao Huang, Hui Xu, Guanqiao He, Yi Lu, Shengyin Tan},
  title = {OpenAvatarChat},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/HumanAIGC-Engineering/OpenAvatarChat}
}
```
