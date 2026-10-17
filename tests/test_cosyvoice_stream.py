import sys
from types import ModuleType, SimpleNamespace as NS

import pytest
import torch

from handlers.tts.cosyvoice.cosyvoice_processor import TTSCosyVoiceProcessor


class StopProcessor(BaseException):
    pass


class InputQueue:
    def __init__(self):
        self.used = False

    def get(self, timeout):
        if self.used:
            raise StopProcessor
        self.used = True
        return dict(text="synthetic speech", key="request", session_id="test")


class OutputQueue:
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)


class CachedVoiceModel:
    def __init__(self):
        self.calls = []

    def inference_zero_shot(self, text, prompt, audio, zero_shot_spk_id="", stream=False):
        self.calls.append((stream, zero_shot_spk_id))
        assert zero_shot_spk_id == ""
        yield {"tts_speech": torch.zeros((1, 8))}

    def inference_sft(self, text, spk_id, stream=False):
        self.calls.append((stream, spk_id))
        yield {"tts_speech": torch.zeros((1, 8))}


class LegacyModel(CachedVoiceModel):
    def inference_zero_shot(self, text, prompt, audio, stream=False):
        self.calls.append((stream, ""))
        yield {"tts_speech": torch.zeros((1, 8))}


def run_processor(monkeypatch, model, fallback=False, reference=True):
    module = ModuleType("cosyvoice_test_model")

    def first_model(**kwargs):
        if fallback:
            raise RuntimeError("Try CosyVoice2")
        return model

    module.CosyVoice = first_model
    module.CosyVoice2 = lambda **kwargs: model
    files = ModuleType("cosyvoice_test_files")
    files.load_wav = lambda path, rate: torch.zeros((1, 16))
    prefix = "handlers.tts.cosyvoice.CosyVoice.cosyvoice."
    monkeypatch.setitem(sys.modules, prefix + "cli.cosyvoice", module)
    monkeypatch.setitem(sys.modules, prefix + "utils.file_utils", files)
    monkeypatch.setattr(sys, "path", sys.path.copy())
    config = NS(
        model_name="synthetic-model",
        api_url=None,
        spk_id="speaker",
        ref_audio_text="synthetic prompt",
        ref_audio_path="reference.wav" if reference else "",
        sample_rate=24000,
        api_key=None,
    )
    output = OutputQueue()
    processor = TTSCosyVoiceProcessor("unused", config, InputQueue(), output)
    with pytest.raises(StopProcessor):
        processor.run()
    return output.items


@pytest.mark.parametrize("model_type", [CachedVoiceModel, LegacyModel])
@pytest.mark.parametrize("fallback", [False, True])
def test_reference_warmup_and_live_calls_request_streaming(monkeypatch, model_type, fallback):
    model = model_type()
    output = run_processor(monkeypatch, model, fallback=fallback)
    assert model.calls == [(True, ""), (True, "")]
    assert output[-1]["tts_speech"] is None
    assert output[-2]["tts_speech"].shape == (1, 8)


def test_sft_nonstreaming_warmup_is_unchanged(monkeypatch):
    model = CachedVoiceModel()
    run_processor(monkeypatch, model, reference=False)
    assert model.calls == [(False, "speaker"), (True, "speaker")]
