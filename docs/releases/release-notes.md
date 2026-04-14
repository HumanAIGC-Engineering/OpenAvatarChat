# 更新日志

## 版本 0.6.0 (2026.04)

- 架构重构，前后端分离，前端仓库 [OpenAvatarChat-WebUI](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)
- 所有数字人均支持手动打断和双工打断模式
- 优化安装部署和模型下载流程，统一依赖管理和模型下载脚本
- 接入 [SoulX-FlashHead](https://github.com/Soul-AILab/SoulX-FlashHead) 数字人，基于扩散模型的实时流式说话头生成

## 版本 0.5.1 (2025.08.19)

- LiteAvatar 支持单机多 session
- 增加对 Qwen-Omni 多模态模型的支持，使用百炼的 Qwen-Omni-Realtime API 服务

## 版本 0.5.0 (2025.08.12)

- 修改为前后端分离版本，前端仓库 [OpenAvatarChat-WebUI](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)
- 增加了对 Dify 的基础调用方式的支持，目前仅支持 chatflow 版本

## 版本 0.4.1 (2025.06.12)

- 增加对 [MuseTalk](https://github.com/TMElyralab/MuseTalk) 数字人的支持，支持自定义形象
- 50 个 LiteAvatar 新形象发布

## 版本 0.3.0 (2025.04.18)

- 增加对 [LAM](https://github.com/aigc3d/LAM) 数字人的支持
- 增加使用百炼 API 的 TTS handler
- 增加对微软 Edge TTS 的支持
- 使用 uv 进行 Python 的包管理

## 版本 0.2.2 (2025.04.14)

- 100 个 LiteAvatar 新形象发布
- 默认使用 GPU 后端运行数字人

## 版本 0.2.1 (2025.04.07)

- 增加历史记录支持
- 支持文本输入
- 启动时不再强制要求摄像头存在
- 优化模块化加载方式

## 版本 0.1.0 (2025.02.20)

- 模块化的实时交互对话数字人，支持云端 API 调用
