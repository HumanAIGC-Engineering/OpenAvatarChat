<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<div align="center">
<strong><a href="README.md">English</a> | 中文</strong>
</div>
<h3 style='text-align: center'>
模块化的交互数字人对话实现，能够在单台PC上运行完整功能。
</h3>
<div style="display: flex; flex-direction: row; justify-content: center">
<a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat" target="_blank"><img alt="Static Badge" style="display: block; padding-right: 5px; height: 20px;" src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"></a>
</div>

## 1. Demo

我们部署了一个服务，音频部分采用SenseVoice + Qwen-VL + CosyVoice实现，
<a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
欢迎体验
    <img alt="Static Badge" style="height: 14px; margin-right: 5px;" src="./assets/images/modelscope_logo.png">。
 </a>
<br>

#### Demo 演示

<video controls src="https://github.com/user-attachments/assets/89753aea-370f-4f10-9d05-f4b104f87dd8">
</video>

## 2. 社区

* 微信群

<img alt="community_wechat.png" height="200" src="assets/images/community_wechat.png" width="200"/>

## 3. 系统需求
* Python版本 3.10+
* 支持CUDA的GPU
* 未量化的多模态语言模型需要20GB以上的显存。
  * 使用int4量化版本的语言模型可以在不到10GB现存的显卡上运行，但可能会因为量化而影响效果。
* 数字人部分使用CPU进行推理，测试设备CPU为i9-13980HX，可以达到30FPS.
> 可以使用云端的LLM模型 api 来替代MiniCPM-o，可以大大减低配置需求，具体可参考 [ASR + LLM + TTS方式](#asr--llm--tts-替代本地-minicpm-o)，这两种模式的结构如下图所示
> <img src="./assets/images/data_flow.svg" />

## 4. 性能
我们在测试PC上记录了回答的延迟时间，10次平均时间约为2.2秒，测试PC使用i9-13900KF和Nvidia RTX 4090。延迟从人的语音结束到数字人的语音开始计算，其中会包括RTC双向传输数据时间、VAD判停延迟以及整个流程的计算时间。

## 5. 组件依赖

|类型|开源项目|Github地址|模型地址|
|---|---|---|---|
|RTC|HumanAIGC-Engineering/gradio-webrtc|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
|VAD|snakers4/silero-vad|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad)||
|LLM|OpenBMB/MiniCPM-o|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)| [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) |
|LLM-int4|||[🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)|
|Avatar|HumanAIGC/lite-avatar|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar)||
|TTS|FunAudioLLM/CosyVoice|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/FunAudioLLM/CosyVoice)||


## 6. 安装

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


#### 下载模型
本项目中大部分的模型与资源文件都包含在引入的子模块中了。多模态语言模型任然需要用户自行下载。本项目目前使用MiniCPM-o-2.6作为多模态语言模型为数字人提供对话能力，用户可以按需从[Huggingface](https://huggingface.co/openbmb/MiniCPM-o-2_6)或者[Modelscope](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6)下载相关模型。建议将模型直接下载到 \<ProjectRoot\>/models/ 默认配置的模型路径指向这里，如果放置与其他位置，需要修改配置文件。scripts目录中有对应模型的下载脚本，可供在linux环境下使用，请在项目根目录下运行脚本：
```bash
scripts/download_MiniCPM-o_2.6.sh
```
```bash
scripts/download_MiniCPM-o_2.6-int4.sh
```

> [!WARNING]
> 本项目支持MiniCPM-o-2.6的原始模型以及int4量化版本，但量化版本需要安装专用分支的AutoGPTQ，相关细节请参考官方的[说明](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)

#### 准备ssl证书
由于本项目使用rtc作为视音频传输的通道，用户如果需要从localhost以为的地方连接服务的话，需要准备ssl证书以开启https，默认配置会读取ssl_certs目录下的localhost.crt和localhost.key，用户可以相应修改配置来使用自己的证书。我们也在scripts目录下提供了生成自签名证书的脚本。需要在项目根目录下运行脚本以使生成的证书被放到默认位置。
```bash
scripts/create_ssl_certs.sh
```

#### 运行
本项目可以以linux容器方式被启动，或者也可以直接启动
  * 容器化运行：容器依赖nvidia的容器环境，在准备好支持GPU的docker环境后，运行以下命令即可完成镜像的构建与启动：
    ```bash
    build_and_run.sh
    ```
  * 直接运行:
    * 安装依赖
    ```bash
    pip install -r requirements.txt
    ```
    * 启动程序
    ```bash
    python src/demo.py
    ```

#### 配置
程序默认启动时，会读取 **<project_root>/configs/chat_with_minicpm.yaml** 中的配置，用户也可以在启动命令后加上--config参数来选择从其他配置文件启动。
```bash
python src/demo.py --config <配置文件的绝对路径>.yaml
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

* 数字人

|参数|默认值|说明|
|---|---|---|
|Tts2Face.avatar_name|sample_data|数字人数据名，目前项目仅提供了"sample_data"可供选择，敬请期待。|
|Tts2Face.fps|25|数字人的运行帧率，在性能较好的CPU上，可以设置为30FPS|
|Tts2Face.enable_fast_mode|True|低延迟模式，打开后可以减低回答的延迟，但在性能不足的情况下，可能会在回答的开始产生语音卡顿。|

> [!IMPORTANT]
> 所有配置中的路径参数都可以使用绝对路径，或者相对于项目根目录的相对路径。

#### ASR + LLM + TTS 替代本地 MiniCPM-o
MiniCPM-o 的本地启动要求相对较高，如果你已有一个可调用的 LLM api_key,可以用这种方式启动来体验对话数字人,修改完后仍可以用 `python src/demo.py` 启动即可
> 如果遇到问题欢迎 [issue](https://github.com/HumanAIGC-Engineering/OpenAvatarChat/issues)给我们

启动配置修改为 ```python src/demo.py --config config/llm_openai_compatible.yaml```
* 修改 config/llm_openai_compatible.yaml 中的 LLM_Bailian配置，代码中的调用方式为 openai 的标准方式，理论上相同的可以兼容

```yaml
LLM_Bailian: 
  moedl_name: "qwen-plus"
  system_prompt: "你是个AI对话数字人，你要用简短的对话来回答我的问题，并在合理的地方插入标点符号"
  api_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```
* 代码内部调用方式
```python
client = OpenAI(
      api_key= self.api_key, 
      base_url=self.api_url,
  )
completion = client.chat.completions.create(
    model=self.model_name,
    messages=[
        self.system_prompt,
        {'role': 'user', 'content': chat_text}
    ],
    stream=True
    )
```
* ASR默认为funasr 调用 iic/SenseVoiceSmall
* LLM默认为百炼api_url + api_key
* TTS默认为CosyVoice的 `iic/CosyVoice-300M-SFT` + `中文女`，可以通过修改为`其他模型`配合 `ref_audio_path` 和 `ref_audio_text` 进行音色复刻

## 7. 社区感谢

感谢社区同学titan909在B站上发布的[部署教程视频](https://www.bilibili.com/video/BV1FNZ8YNEA8)


## 8. 贡献者

[程刚](https://github.com/lovepope)
[陈涛](https://github.com/raidios)
[王丰](https://github.com/sudowind)
[黄斌超](https://github.com/bingochaos)
[徐辉](https://github.com/xhup)
[何冠桥](https://github.com/bboygun)
[卢益](https://github.com/HaveAnApplePie)

## 9. Star历史

如果您觉得我们的项目还有点帮助，辛苦帮我们点个⭐，感谢！
![](https://api.star-history.com/svg?repos=HumanAIGC-Engineering/OpenAvatarChat&type=Date)