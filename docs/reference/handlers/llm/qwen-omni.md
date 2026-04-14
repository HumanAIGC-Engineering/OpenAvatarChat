# Qwen-Omni 多模态语言模型 Handler

使用百炼的 API 来接入 Qwen-Omni 的能力。当前仅支持 manual 模式，VAD 由本地的 SileroVAD 模型执行。

由于 manual 模式下 ASR 的结果非常差且不可靠，因此额外增加了 SenseVoice 模块仅用于回显对话记录。

完整配置文件可以参考 `chat_with_qwen_omni.yaml`，其中 Avatar 模块可以在 MuseTalk 和 LiteAvatar 之间选择。
