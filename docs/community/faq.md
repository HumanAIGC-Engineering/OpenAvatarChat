# 常见问题

> [!NOTE]
> 请避免创建与下述问题有关的 issues，这些 issues 可能不会被回复。

## 部署相关

### 环境配置

**Q: 项目支持哪些操作系统？**

目前支持 Linux 和 Windows。LAM 模块可以在 Mac 上运行，只需移除 CUDA 相关的依赖（如 `onnxruntime-gpu`），即可在 CPU 上运行。

---

**Q: 安装 onnxruntime-gpu 失败怎么办？**

1. 确认 CUDA 版本兼容性
2. 检查 Python 版本是否匹配
3. 尝试使用 conda 环境安装
4. 注意平台兼容性（manylinux_2_27_x86_64、manylinux_2_28_x86_64、win_amd64）

---

**Q: 50 系显卡是否支持？**

目前 50 系显卡需要使用 CUDA 12.8 以上，对应 pytorch 相关的包需要安装 12.8 版本：

```bash
# https://pytorch.org/get-started/locally/
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

---

**Q: 纯 CPU 或 Mac 机器是否能部署？**

目前只能顺畅运行 `config/chat_with_lam.yaml`，LiteAvatar 暂时无法在纯 CPU 上运行。Mac 用户可能需要手动将所有 device 改为 mps。

运行 `chat_with_lam.yaml` 所需额外步骤：

1. 移除 `torchvision` 依赖
2. 将 `onnxruntime-gpu` 替换为 `onnxruntime`
3. 修改 `src/handlers/avatar/lam/LAM_Audio2Expression/engines/infer.py`，删除所有 `.cuda()` 调用
4. 按照 README 安装依赖后运行

---

**Q: pynini 安装出现问题怎么办？**

查看 README 中关于 CosyVoice 模块安装的部分。

---

**Q: 安装报错 fastrtc-0.0.19.dev0-py3-none-any.whl 不存在**

这个报错说明子模块没有全部拉下来，在项目根目录重新拉取子模块：

```bash
git submodule update --init --recursive --depth 1
```

---

**Q: Windows 下出现 'gbk' 编码相关的错误**

手动设置环境变量 `PYTHONUTF8=1`。

---

**Q: 使用 pip install 安装 requirements.txt 后部署运行报错**

项目依赖以模块化的方式存放，根目录下的 `requirements.txt` 只包含公共依赖。请使用 `uv` 进行依赖安装，或者根据需要用到的模块下的 `.toml` 文件手动安装所需模块的对应依赖。

### 部署问题

**Q: AutoDL 部署了 TURN Server 之后还是不能远程打开？**

AutoDL 不支持个人用户开启自定义端口，无法远程登录。

## 运行相关

**Q: 运行过程中 session 意外停止，但日志中并没有明显异常**

RTC Handler 中有 session 的时长限制，参数名是 `connection_ttl`，默认值为 900 秒（15 分钟），可在 Client Handler 配置中修改。

## 语音相关

**Q: 语音模型卡顿怎么解决？**

如果使用本地 CosyVoice，请检查 GPU 显存使用情况，可在配置文件中调整批处理大小，或改为 API 调用。如果是 API 调用卡顿，请排查网络问题和 API 本身的返回延迟。

---

**Q: 语音识别不准确怎么办？**

1. 检查麦克风设置
2. 确保环境噪音较小
3. 调整语音识别参数

## 功能使用

**Q: 如何自定义数字人外观？**

LiteAvatar 暂不支持自定义，但可以使用[官方形象库](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)。LAM 数字人支持自定义，参考对应的 [Git 项目地址](https://github.com/aigc3d/LAM)。

---

**Q: 如何更换数字人模型？**

找到对应想修改的角色，然后更换 config 文件中对应的形象参数。

---

**Q: 怎么开启模型的视觉功能？**

在 API 调用时选择具有视觉功能的 model id（如 `qwen_vl`），或使用本地的多模态模型。具体实现是将用户对话时摄像头捕获到的最后一帧画面一起提交给 LLM。

---

**Q: 项目目前支持多路并发吗？**

目前 LiteAvatar 数字人不支持多路并发，LAM 数字人支持多路并发，可以在对应配置文件中修改。

---

**Q: 前端代码在哪里？**

在 git submodule 中的 `gradio_webrtc`，这个组件包含了 WebRTC 功能的封装和 UI 相关的代码。

路径：`OpenAvatarChat/src/third_party/gradio_webrtc_videochat`

---

**Q: 如何配置 TURN Server？**

参考 [部署要求](/guide/deployment) 中关于 TURN Server 配置的说明。

## 最佳实践

1. 使用官方推荐的配置环境
2. 拉取最新代码
3. 做好环境隔离，使用 `uv` 进行依赖管理和配置

> [!TIP]
> 若使用最新的代码仍然无法解决问题，请创建一个 [Issue](https://github.com/HumanAIGC-Engineering/OpenAvatarChat/issues)。
