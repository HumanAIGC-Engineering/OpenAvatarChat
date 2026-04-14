"""
Audio utilities module.

This module provides consolidated audio processing utilities including
automatic gain control, A-weighting filters, and mel-spectrum analysis.
"""

from .common_audio_utils import (
    AudioUtils,
)
from .auto_gain_control import (
    AutoGainControl,
    RMSAGC,
    MelSpectrumAGC,
    create_agc,
    create_rms_agc,
    create_mel_agc
)

__all__ = [
    'AudioUtils',
    'AutoGainControl', 
    'RMSAGC',
    'MelSpectrumAGC',
    'create_agc',
    'create_rms_agc',
    'create_mel_agc'
]
