# LAM Avatar Driver Handler

## Model Dependencies

```bash
uv run scripts/download_models.py --handler lam
uv run scripts/download_models.py --handler lam --source modelscope
```

<details>
<summary>Manual Download</summary>

* **facebook/wav2vec2-base-960h**
```bash
git clone --depth 1 https://huggingface.co/facebook/wav2vec2-base-960h ./models/wav2vec2-base-960h
```

* **LAM_audio2exp**
```bash
wget https://huggingface.co/3DAIGC/LAM_audio2exp/resolve/main/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
tar -xzvf ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar -C ./models/LAM_audio2exp
```

</details>
