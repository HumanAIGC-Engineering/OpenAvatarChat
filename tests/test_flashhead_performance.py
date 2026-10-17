from types import SimpleNamespace as NS

import numpy as np
import pytest
import torch

from handlers.avatar.flashhead.flashhead_config import FlashHeadConfig
from handlers.avatar.flashhead.flashhead_processor import FlashHeadProcessor


@pytest.mark.parametrize("dtype", [torch.float32, torch.float16])
def test_quantization_preserves_existing_output_values(dtype):
    sample = torch.tensor([-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0], dtype=dtype).reshape(1, 7, 1, 1)
    p = object.__new__(FlashHeadProcessor)
    p.pipeline = NS(device="cpu", generate=lambda embedding: sample)
    actual = p._run_pipeline(torch.zeros(1))
    previous = (((sample + 1) / 2).permute(1, 2, 3, 0).clip(0, 1) * 255).contiguous()
    assert actual.dtype == torch.uint8
    assert np.array_equal(actual.numpy(), previous.numpy().astype(np.uint8))


def test_compile_remains_disabled_by_default():
    assert FlashHeadConfig().enable_compile is False
    assert FlashHeadConfig(enable_compile=True).enable_compile is True
