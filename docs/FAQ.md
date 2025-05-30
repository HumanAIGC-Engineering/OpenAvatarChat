# 🚨FAQs | 常见问题🚨

> [!NOTE]
> Please avoid creating issues regarding the following questions, as they might be closed without a response.
> 
> 请避免创建与下述问题有关的 issues，这些 issues 可能不会被回复。


## Deployment Related Issues / 部署相关问题

### Environment Configuration / 环境配置

**Q: What operating systems are supported by the project? / 项目支持哪些操作系统**  

Currently supports Linux and Windows.  
目前支持Linux和Windows。

```
The LAM can be run on a mac, just remove cuda related dependencies like onnxruntime-gpu to run on a cpu!
LAM 部分可以使用mac运行，只需移除cuda 相关的依赖，比如onnxruntime-gpu，就可以在cpu 上运行
```

### Dependency Installation / 依赖安装

**Q: How to resolve onnxruntime-gpu installation failure? / 安装 onnxruntime-gpu 失败怎么办？**  

1. Verify CUDA version compatibility  
2. Check Python version compatibility  
3. Try installing via conda environment  
4. Pay attention to platform compatibility (manylinux_2_27_x86_64, manylinux_2_28_x86_64, win_amd64)  
<!-- new list start -->

1. 确认 CUDA 版本兼容性  
2. 检查 Python 版本是否匹配  
3. 尝试使用 conda 环境安装  
4. 注意平台兼容性（manylinux_2_27_x86_64, manylinux_2_28_x86_64, win_amd64）

---

**Q: Is RTX 50 supported / 50系显卡是否支持**
Currently, 50 series need to use cuda12.8 or above, the corresponding pytorch-related packages need to be installed as version 12.8.
目前50系显卡需要使用cuda12.8以上，对应pytorch相关的包需要安装成12.8的版本
```
#https://pytorch.org/get-started/locally/
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```
---

**Q: How to resolve pynini installation issues? / pynini 安装出现问题怎么办？**  

Refer to the cosyvoice module installation section in README.  
查看readme中关于cosyvoice模块安装的部分。

---

**Q: Error: fastrtc-0.0.19.dev0-py3-none-any.whl not found during installation / 安装报错文件fastrtc-0.0.19.dev0-py3-none-any.whl不存在**  

This error indicates incomplete submodule retrieval. Re-pull submodules from the project root directory.  
这个报错说明子模块没有全部拉下来。在项目根目录重新拉取子模块。

---

**Q: Error related to 'gbk' encoding on Windows / windows下出现'gbk'编码相关的错误**

Manually set environment variable PYTHONUTF8=1.  
可以手动设置环境变量PYTHONUTF8=1。

---

**Q: Error when running deployment after pip install requirements.txt / 使用pip install安装对应的requirements.txt，部署运行时报错**  

Project dependencies are modularized. The root requirements.txt contains only public dependencies. Use uv for installation, or manually install required module dependencies based on .toml files.  
项目依赖以模块化的方式存放，根目录下的requirements.txt只包含公共依赖。请使用uv进行依赖安装，或者根据需要用到的模块下的.toml文件，手动安装所需模块的对应依赖。

### Deployment Issues / 部署问题

**Q: AutoDL deployment of TURN Server fails to enable remote access? / AutoDL部署了TURN Server之后还是不能远程打开？**  

AutoDL does not allow personal users to open custom ports, remote login unavailable.  
AutoDL不支持个人用户开启自定义端口，无法远程登录。

## Runtime Related Issues / 运行相关问题

### Performance Issues / 性能问题

**Q: Intermittent lag when using minicpm as LLM on 4090 / 4090下使用minicpm作为llm，对话过程中时不时存在卡顿**

Non-quantized minicpm shows lag on 4090. Recommend switching LLM to API call or using non-multimodal local models.  
minicpm非量化版本在4090上测试下来是会存在卡顿，建议llm改用api调用，或者本地的非多模态模型。

## Audio Related Issues / 语音相关问题

### TTS Model / TTS 模型

**Q: How to resolve audio model lag? / 语音模型卡顿怎么解决？** 

For local cosyvoice, check GPU memory usage and adjust batch size in config. Switch to API call if needed. For API lag, check network issues and API response latency.  
如果调用的是本地的cosyvoice，请检查GPU显存使用情况，可以在配置文件中调整批处理大小。或者改为API调用。如果是API调用卡顿，请排查网络问题和API本身的调用返回延迟。

### Audio Interaction / 语音交互

**Q: How to improve speech recognition accuracy? / 语音识别不准确怎么办？**  

1. Check microphone settings  
2. Ensure low ambient noise  
3. Adjust speech recognition parameters  
<!-- new list start -->

1. 检查麦克风设置  
2. 确保环境噪音较小  
3. 调整语音识别参数

## Feature Usage / 功能使用

### Digital Human / 数字人

**Q: How to customize digital human appearance? / 如何自定义数字人外观？**

LiteAvatar does not support customization but provides [official character library](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery). LAM supports customization via [Git project](https://github.com/aigc3d/LAM).  
LiteAvatar暂不支持自定义，但可以使用[官方形象库](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)。LAM 数字人支持自定义，参考对应的[git项目地址](https://github.com/aigc3d/LAM)。

---

**Q: How to change digital human models? / 如何更换数字人模型？**  

Locate the target character and modify the appearance parameters in config file.  
找到对应想修改的角色，然后更换config文件中对应的形象参数。

---

**Q: How to enable model vision capabilities and how are they implemented? / 怎么开启模型的视觉功能。模型的视觉具体是如何实现的** 

Select model IDs with vision capabilities like qwen_vl via API, or use local multimodal models. Implementation combines LLM with the last captured video frame during user interaction.  
在api调用时选择具有视觉功能的model id如qwen_vl，或使用本地的多模态模型。具体实现是将用户对话时摄像头捕获到的最后一帧画面一起提交给llm。

---

**Q: Does the project support multi-channel concurrency? / 项目目前支持多路并发吗？**

LiteAvatar does not support concurrency while LAM supports it via configuration file changes.  
目前LiteAvatar数字人不支持多路并发，LAM数字人支持多路并发，可以在对应配置文件中修改。

---
**Q: Where is the front-end code? / 前端代码在哪里？**
gradio_webrtc in the git submodule, which contains wrappers for webrtc functionality and UI-related code
git submodule 中的 gradio_webrtc，这个组件包含了webrtc 功能的封装和 UI 相关的代码

Path：OpenAvatarChat\src\third_party\gradio_webrtc_videochat
Link： https://github.com/HumanAIGC-Engineering/gradio-webrtc.git

### Integrated Features / 集成功能

**Q: How to configure Turn Server? / 如何配置 Turn Server？**  

Refer to Turn Server configuration README.  
参考Turn Server配置的readme。


## Best Practices / 最佳实践

1. Use officially recommended configuration environment  
2. Pull latest code  
3. Maintain environment isolation using uv for dependency management  
<!-- new list start -->

1. 使用官方推荐的配置环境  
2. 拉取最新代码  
3. 做好环境隔离，使用uv进行依赖管理和配置

> [!Tip]
> If the problems still exist with the latest code, please create an issue.
> 若使用最新的代码仍然无法解决问题，请创建一个 issue。
