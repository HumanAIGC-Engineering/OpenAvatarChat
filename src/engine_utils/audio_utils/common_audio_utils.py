from typing import Tuple, Optional

import librosa
import numpy as np
from scipy.signal import bilinear, lfilter


class AudioUtils:
    """Consolidated audio utility functions."""
    
    @staticmethod
    def get_a_weighting_curve(freq: int = 48000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Design of an A-weighting filter.
        b, a = A_weighting(fs) designs a digital A-weighting filter for
        sampling frequency `fs`. Usage: y = scipy.signal.lfilter(b, a, x).
        Warning: `fs` should normally be higher than 20 kHz. For example,
        fs = 48000 yields a class 1-compliant filter.
        References:
           [1] IEC/CD 1672: Electroacoustics-Sound Level Meters, Nov. 1996.
        """
        # Definition of analog A-weighting filter according to IEC/CD 1672.
        f1 = 20.598997
        f2 = 107.65265
        f3 = 737.86223
        f4 = 12194.217
        A1000 = 1.9997

        NUMs = [(2 * np.pi * f4) ** 2 * (10 ** (A1000 / 20)), 0, 0, 0, 0]
        DENs = np.polymul([1, 4 * np.pi * f4, (2 * np.pi * f4) ** 2],
                       [1, 4 * np.pi * f1, (2 * np.pi * f1) ** 2])
        DENs = np.polymul(np.polymul(DENs, [1, 2 * np.pi * f3]),
                       [1, 2 * np.pi * f2])

        # Use the bilinear transformation to get the digital filter.
        return bilinear(NUMs, DENs, freq)
    
    @staticmethod
    def get_rms(audio: np.ndarray, weight_curve: Optional[Tuple[np.ndarray, np.ndarray]] = None) -> float:
        """Calculate RMS with optional A-weighting."""
        if weight_curve is not None:
            b, a = weight_curve
            audio = lfilter(b, a, audio)
        return np.sqrt(np.mean(np.absolute(audio) ** 2))
    
    @staticmethod
    def rms_to_db(rms_value: float) -> float:
        """Convert RMS value to dB."""
        return 20 * np.log10(max(rms_value, 1e-10))
    
    @staticmethod
    def db_to_linear(db_value: float) -> float:
        """Convert dB to linear scale."""
        return 10.0 ** (db_value / 20.0)
    
    @staticmethod
    def compute_mel_spectrogram(
        audio: np.ndarray, 
        sr: int = 16000, 
        n_mels: int = 80, 
        n_fft: int = 1024, 
        hop_length: int = 256,
        fmin: float = 0.0,
        fmax: Optional[float] = None
    ) -> np.ndarray:
        """Compute mel spectrogram using librosa."""
        if fmax is None:
            fmax = sr // 2
        return librosa.feature.melspectrogram(
            y=audio, sr=sr, n_mels=n_mels, n_fft=n_fft, 
            hop_length=hop_length, fmin=fmin, fmax=fmax
        )

