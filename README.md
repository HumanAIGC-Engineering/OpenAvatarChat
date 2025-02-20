<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<div align="center">
<strong>中文|<a href="./readme_en.md">English</a></strong>
</div>
<h3 style='text-align: center'>
模块化的交互数字人对话实现，能够在单台PC上运行完整功能。
</h3>
<div style="display: flex; flex-direction: row; justify-content: center">
<a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat" target="_blank"><img alt="Static Badge" style="display: block; padding-right: 5px; height: 20px;" src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"></a>
</div>

## 系统需求
* Python版本 3.10+
* 支持CUDA的GPU
* 未量化的多模态语言模型需要20GB以上的显存。
  * 使用int4量化版本的语言模型可以在不到10GB现存的显卡上运行，但可能会因为量化而影响效果。
* 数字人部分使用CPU进行推理，测试设备CPU为i9-13980HX，可以达到30FPS.

## 性能
我们在测试PC上记录了回答的延迟时间，10次平均时间约为2.2秒，测试PC使用i9-13900KF和Nvidia RTX 4090。延迟从人的语音结束到数字人的语音开始计算，其中会包括RTC双向传输数据时间、VAD判停延迟以及整个流程的计算时间。

## 组件依赖

|类型|开源项目|Github地址|模型地址|
|---|---|---|---|
|RTC|HumanAIGC-Engineering/gradio-webrtc|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
|VAD|snakers4/silero-vad|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad)||
|LLM|OpenBMB/MiniCPM-o|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)| [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) |
|LLM-int4|||[🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)|
|Avatar|HumanAIGC/lite-avatar|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar)||


## 安装
**注意1：本项目子模块以及依赖模型都需要使用git lfs模块，请确认lfs功能已安装**
```bash
sudo apt install git-lfs
git lfs install 
```
**注意2：本项目通过git子模块方式引用三方库，运行前需要更新子模块**
```bash
git submodule update --init --recursive
```
#### 下载模型
本项目中大部分的模型与资源文件都包含在引入的子模块中了。多模态语言模型任然需要用户自行下载。本项目目前使用MiniCPM-o-2.6作为多模态语言模型为数字人提供对话能力，用户可以按需从[Huggingface](https://huggingface.co/openbmb/MiniCPM-o-2_6)或者[Modelscope](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6)下载相关模型。建议将模型直接下载到 \<ProjectRoot\>/models/ 默认配置的模型路径指向这里，如果放置与其他位置，需要修改配置文件。scripts目录中有对应模型的下载脚本，可供在linux环境下使用，请在项目根目录下运行脚本：
```bash
scripts/download_MiniCPM-o_2.6.sh
```
```bash
scripts/download_MiniCPM-o_2.6-int4.sh
```
**注意：本项目支持MiniCPM-o-2.6的原始模型以及int4量化版本，但量化版本需要安装专用分支的AutoGPTQ，相关细节请参考官方的[说明](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)**

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
程序默认启动时，会读取 **<project_root>/configs/sample.yaml** 中的配置，用户也可以在启动命令后加上--config参数来选择从其他配置文件启动。
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

|参数|默认值|说明|
|---|---|---|
|S2S_MiniCPM.model_name|MiniCPM-o-2_6|该参数用于选择使用的语言模型，可选"MiniCPM-o-2_6" 或者 "MiniCPM-o-2_6-int4"，需要确保model目录下实际模型的目录名与此一致。|
|S2S_MiniCPM.voice_prompt||MiniCPM-o的voice prompt|
|S2S_MiniCPM.assistant_prompt||MiniCPM-o的assistant prompt|

* 数字人

|参数|默认值|说明|
|---|---|---|
|Tts2Face.avatar_name|sample_data|数字人数据名，目前项目仅提供了"sample_data"可供选择，敬请期待。|
|Tts2Face.fps|25|数字人的运行帧率，在性能较好的CPU上，可以设置为30FPS|
|Tts2Face.enable_fast_mode|True|低延迟模式，打开后可以减低回答的延迟，但在性能不足的情况下，可能会在回答的开始产生语音卡顿。|

**注意：所有配置中的路径参数都可以使用绝对路径，或者相对于项目根目录的相对路径。**
