

<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<div align="center">
<strong><a href=./README.md>中文</a>|English</strong>
</div>
<h3 style='text-align: center'>
A modular avatar chat implementation runs on single pc.
</h3>
<div style="display: flex; flex-direction: row; justify-content: center">

<a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat" target="_blank"><img alt="Static Badge" style="display: block; padding-right: 5px; height: 20px;" src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"></a>
</div>

## Requirements
* Need Python 3.10+
* Cuda capable GPU
* 20GB+ VRam needed to load omni-llm model without quantization. 
  * Less than 10GB VRam is sufficient for int4 quantization, but the response quality may be limited.
* Avatar part use CPU to inference, reaches 30fps on an i9-13980HX.

**Note: All path in the config file can be absolute path or path relative to the project root.**
## Performance
Response delay is around 2.2 seconds averaged by 10 measturements on test pc (i9-13900KF and Nvidia RTX 4090).
It's counted between human voice end and subsequent avatar audio starts, which includes bidirectional rtc delay, vad delay and the pipeline computation time.

## Components Dependency

|Type|Project|Github|Model|
|---|---|---|---|
|RTC|HumanAIGC-Engineering/gradio-webrtc|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
|VAD|snakers4/silero-vad|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad)||
|LLM|OpenBMB/MiniCPM-o|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)| [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) |
|LLM-int4|||[🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)|
|Avatar|HumanAIGC/lite-avatar|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar)||

## Installation
**Note1：Submodules referred by this project and the models all need git lfs module to be cloned properly, please install it before clone any code.**
```bash
sudo apt install git-lfs
git lfs install 
```
**Note2: third party projects are included by submodule, remember to update submodules.**
```bash
git submodule update --init --recursive
```
#### Download model
Most model and resource files are included in the submodules of this project, except for the LLM model, we currently use MiniCPM-o-2.6 as the omni language model, user can download the model files from Huggingface or Modelscope. Models are recommended to be downloaded into \<ProjectRoot\>/models/, otherwise the default config should be altered. Helper scripts in scripts folder are provided to download corresponding model. Run them under project root.
```bash
scripts/download_MiniCPM-o_2.6.sh
```
```bash
scripts/download_MiniCPM-o_2.6-int4.sh
```
**Note: Both full precision version and the int4 quantized one are supported. However，the int4 version need a special version of AutoGPTQ to load, refer to the [model card](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4) please.**

#### Prepare ssl certificates.
Since we use rtc to stream the video and audio, if not linked from localhost an ssl certificates is needed, user can put exist ones into the ssl_certs folder and config them in the config file or create a new self signed one with the provided script. Run the script under project root to put the result into proper position.
```bash
scripts/create_ssl_certs.sh
```

#### Run the demo
Demo can be start in a linux container or start in host os.
  * Run in container: After prepared GPU capable docker environment, run the following script to build and start the service.
    ```bash
    build_and_run.sh
    ```
  * Run directly:
    * Install requirements
    ```bash
    pip install -r requirements.txt
    ```
    * Start demo
    ```bash
    python src/demo.py
    ```

#### Configs
The default parameter will load config from **<project_root>/configs/sample.yaml**. Config can be loaded from other file by add the --config parameter.
```bash
python src/demo.py --config <absolute-path-to-the-config>.yaml
```
Configurable parameters are listed here：
|Parameter|Default|Description|
|---|---|---|
|log.log_level|INFO|Log level of the demo.|
|service.host|0.0.0.0|Address to start gradio application on.|
|service.port|8282|Port to start gradio application on.|
|service.cert_file|ssl_certs/localhost.crt|Certificate file for ssl, if both cert_file and cert_key are found, https will be enabled.|
|service.cert_key|ssl_certs/localhost.key|Certificate file for ssl, if both cert_file and cert_key are found, https will be enabled.|
|chat_engine.model_root|models|Path to find models.|
|chat_engine.handler_configs|N/A|Handler configs are provided by each handler.|

Current implemented handler provide following configs:
* VAD

|Parameter|Default|Description|
|---|---|---|
|SileraVad.speaking_threshold|0.5|Threshold to determine whether user starts speaking or end speaking.|
|SileraVad.start_delay|2048|Speaking probability should be higher than threshold longer than this period to be recognized as start of speaking, unit in audio sample.|
|SileraVad.end_delay|2048|Speaking probability should be lower than threshold longer than this period to be recognized as end of speaking, unit in audio sample.|
|SileraVad.buffer_look_back|1024|For high threshold, the very start part to the voice may be clipped, use this to compensate, unit in audio sample.|
|SileraVad.speech_padding|512|Silence of this length will be padded on both start and end, unit in audio sample.|

* LLM

|Parameter|Default|Description|
|---|---|---|
|S2S_MiniCPM.model_name|MiniCPM-o-2_6|Which model to load, can be "MiniCPM-o-2_6" or "MiniCPM-o-2_6-int4", it should match the folder's name under model directory.|
|S2S_MiniCPM.voice_prompt||Voice prompt for MiniCPM-o.|
|S2S_MiniCPM.assistant_prompt||Assistant prompt for MiniCPM-o.|

* Avatar

|Parameter|Default|Description|
|---|---|---|
|Tts2Face.avatar_name|sample_data|Avatar data name, currently only the sample data is provided.|
|Tts2Face.fps|25|Framerate of avatar, on better CPU, it can be set to 30.|
|Tts2Face.enable_fast_mode|True|Lower the response delay, voice lag may occur if computation power is not enough.|

## Contributors

[Gang Cheng](https://github.com/lovepope)
[Tao Chen](https://github.com/raidios)
[Feng Wang](https://github.com/sudowind)
[Binchao Huang](https://github.com/bingochaos)
[Hui Xu](https://github.com/xhup)
[Guanqiao He](https://github.com/bboygun)
