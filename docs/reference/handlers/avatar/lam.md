# LAM 数字人驱动 Handler

## 依赖模型

```bash
uv run scripts/download_models.py --handler lam
# 国内用户推荐：
uv run scripts/download_models.py --handler lam --source modelscope
```

<details>
<summary>手动下载</summary>

* **facebook/wav2vec2-base-960h** [HuggingFace](https://huggingface.co/facebook/wav2vec2-base-960h) / [ModelScope](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)

```bash
# HuggingFace
git clone --depth 1 https://huggingface.co/facebook/wav2vec2-base-960h ./models/wav2vec2-base-960h
# ModelScope（国内推荐）
git clone --depth 1 https://www.modelscope.cn/AI-ModelScope/wav2vec2-base-960h.git ./models/wav2vec2-base-960h
```

* **LAM_audio2exp** [HuggingFace](https://huggingface.co/3DAIGC/LAM_audio2exp)

```bash
# HuggingFace
wget https://huggingface.co/3DAIGC/LAM_audio2exp/resolve/main/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
tar -xzvf ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar -C ./models/LAM_audio2exp && rm ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar

# 阿里云 OSS
wget https://virutalbuy-public.oss-cn-hangzhou.aliyuncs.com/share/aigc3d/data/LAM/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
tar -xzvf ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar -C ./models/LAM_audio2exp && rm ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar
```

</details>
