# FlashHead 独立推理进程（实验候选）

默认仍为 `in_process`，不改变默认 eager 执行方式。`process` 使用 spawn 子进程持有模型，完成真实预热后返回就绪；单槽共享内存通过串行请求与父进程复制防止覆盖。

进程模式仅支持 engine `concurrent_limit: 1`。配置、生命周期边界和 GPU 验证步骤见 [完整说明](../../../en/reference/handlers/avatar/flashhead-worker.md)。

输出队列以音视频配对为单位背压，容量至少为一批，或 `ceil(max_buffer_seconds * fps)`，取较大值。取消以 generation 丢弃迟到结果；待机视频配对静音。引擎和 RTC 并非全面有界，也无法撤回浏览器已经缓存的媒体。

仍要求模型输入 16 kHz、25 FPS；默认输出 24 kHz，保留其他能与帧时钟整除的正采样率。worker 异常或超时后关闭，不自动重启或静默回退，需要重启服务恢复。

CPU 回归使用合成后端，覆盖真实多进程与共享内存、预热协议、背压、打断、时钟配对及异常清理。不代表已加载真实模型，也不代表 GPU 验收通过。待机配对静音也影响 in-process FlashHead，实际客户端行为需要端到端验收。

GPU 测试尚未完成；此候选没有宣称延迟、吞吐或显存改善。其他 Avatar 源码没有修改。
