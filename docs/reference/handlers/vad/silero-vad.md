# SileroVAD Handler

使用 Silero 模型进行语音活动检测。

## 配置参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| SileraVad.speaking_threshold | 0.5 | 判定输入音频为语音的阈值 |
| SileraVad.start_delay | 2048 | 持续大于阈值超过此时间后判定为说话开始（音频采样数） |
| SileraVad.end_delay | 2048 | 持续小于阈值超过此时间后判定为说话结束（音频采样数） |
| SileraVad.buffer_look_back | 1024 | 语音起始点往前回溯的时间（音频采样数） |
| SileraVad.speech_padding | 512 | 在起始与结束两端加上的静音长度（音频采样数） |
