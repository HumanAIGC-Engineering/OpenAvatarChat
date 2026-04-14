# LiteAvatar 数字人 Handler

集成 LiteAvatar 算法生成 2D 数字人，在 ModelScope 的 [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery) 中提供了 100 个数字人形象可供使用。

## 依赖模型

```bash
uv run scripts/download_models.py --handler liteavatar
```

也可以使用独立脚本：
```bash
bash scripts/download_liteavatar_weights.sh
```

## 配置参数

```yaml
LiteAvatar:
  module: avatar/liteavatar/avatar_handler_liteavatar
  avatar_name: 20250408/sample_data
  fps: 25
  use_gpu: true
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| LiteAvatar.avatar_name | 20250408/sample_data | 数字人数据名 |
| LiteAvatar.fps | 25 | 数字人的运行帧率 |
| LiteAvatar.enable_fast_mode | False | 低延迟模式 |
| LiteAvatar.use_gpu | True | 是否使用 GPU |

## 多 session 支持

LiteAvatar 支持单机多 session。设置 `default.chan_engine.concurrent_limit` 即可声明最大并发路数。

> [!WARNING]
> 每一路并发大约占用 3G 显存，`concurrent_limit` 设置过大可能导致显存溢出。
