# SileroVAD Handler

Voice activity detection using the Silero model.

## Configuration

| Parameter | Default | Description |
|---|---|---|
| SileraVad.speaking_threshold | 0.5 | Threshold for speech detection |
| SileraVad.start_delay | 2048 | Samples above threshold before speech start |
| SileraVad.end_delay | 2048 | Samples below threshold before speech end |
| SileraVad.buffer_look_back | 1024 | Lookback samples to avoid clipping |
| SileraVad.speech_padding | 512 | Silence padding on both ends |
