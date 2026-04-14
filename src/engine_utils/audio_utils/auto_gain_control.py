"""
Automatic Gain Control (AGC) for streaming audio processing.

This module provides a streaming AGC implementation that maintains consistent
audio levels across variable input volumes while preserving the original audio
characteristics and shape. Based on time-frequency analysis using mel-spectrograms
inspired by the pyagc project.
"""

import numpy as np
from typing import Dict, Any, Optional
from collections import deque
from loguru import logger
from scipy.signal import lfilter

from engine_utils.audio_utils import AudioUtils


class MelSpectrumAGC:
    """
    Time-Frequency Automatic Gain Control using mel-spectrograms.
    
    This class implements AGC based on mel-spectrum analysis, inspired by
    the pyagc project. It provides more sophisticated frequency-domain
    processing compared to simple RMS-based AGC.
    
    Features:
    - Mel-spectrum based gain calculation
    - Frequency-dependent gain adjustment
    - Streaming processing with state preservation
    - A-weighting support for perceptual accuracy
    """
    
    def __init__(
        self,
        target_level_db: float = -20.0,
        max_gain_db: float = 20.0,
        min_gain_db: float = -20.0,
        attack_time_ms: float = 10.0,
        release_time_ms: float = 100.0,
        sample_rate: int = 16000,
        n_mels: int = 80,
        n_fft: int = 1024,
        hop_length: int = 256,
        mel_window_ms: float = 100.0,
        use_a_weighting: bool = True,
        noise_gate_db: float = -40.0
    ):
        """
        Initialize the Mel-Spectrum AGC.
        
        Args:
            target_level_db: Target level in dB
            max_gain_db: Maximum gain in dB
            min_gain_db: Minimum gain in dB
            attack_time_ms: Attack time in milliseconds
            release_time_ms: Release time in milliseconds
            sample_rate: Audio sample rate in Hz
            n_mels: Number of mel bins
            n_fft: FFT size
            hop_length: Hop length for STFT
            mel_window_ms: Mel analysis window in milliseconds
            use_a_weighting: Whether to use A-weighting
            noise_gate_db: Noise gate threshold in dB
        """
        self.target_level_db = target_level_db
        self.target_level_linear = AudioUtils.db_to_linear(target_level_db)
        self.max_gain_db = max_gain_db
        self.min_gain_db = min_gain_db
        self.sample_rate = sample_rate
        self.n_mels = n_mels
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.noise_gate_db = noise_gate_db
        self.noise_gate_linear = AudioUtils.db_to_linear(noise_gate_db)
        
        # Calculate time constants
        self.attack_alpha = self._calculate_alpha(attack_time_ms)
        self.release_alpha = self._calculate_alpha(release_time_ms)
        
        # Mel analysis parameters
        self.mel_window_samples = int(mel_window_ms * sample_rate / 1000.0)
        
        # A-weighting setup
        self.use_a_weighting = use_a_weighting
        self.a_weighting_curve = None
        if use_a_weighting:
            self.a_weighting_curve = AudioUtils.get_a_weighting_curve(sample_rate)
        
        # State variables
        self.current_gain_db = 0.0
        self.mel_buffer = deque()
        self.mel_buffer_filled = False
        
        logger.debug(f"MelSpectrumAGC initialized: target={target_level_db}dB, "
                   f"n_mels={n_mels}, n_fft={n_fft}, hop_length={hop_length}")
    
    def warmup(self) -> None:
        """Warmup the AGC to avoid first-time loading costs affecting performance measurements."""
        logger.debug("MelSpectrumAGC warmup started...")
        
        # Create dummy audio for warmup
        dummy_audio = np.random.randn(self.hop_length * 4).astype(np.float32)  # 4 hop lengths
        
        # Warmup mel spectrogram computation
        try:
            _ = AudioUtils.compute_mel_spectrogram(
                dummy_audio, self.sample_rate, self.n_mels, 
                self.n_fft, self.hop_length
            )
            logger.debug("MelSpectrumAGC warmup completed successfully")
        except Exception as e:
            logger.warning(f"MelSpectrumAGC warmup failed: {e}")
        
        # Warmup A-weighting filter if enabled
        if self.use_a_weighting and self.a_weighting_curve is not None:
            try:
                b, a = self.a_weighting_curve
                _ = lfilter(b, a, dummy_audio)
                logger.debug("A-weighting filter warmup completed")
            except Exception as e:
                logger.warning(f"A-weighting filter warmup failed: {e}")
    
    def _calculate_alpha(self, time_ms: float) -> float:
        """Calculate alpha coefficient for exponential smoothing."""
        if time_ms <= 0:
            return 1.0
        return np.exp(-1.0 / (time_ms * self.sample_rate / 1000.0))
    
    def _update_mel_buffer(self, audio_chunk: np.ndarray) -> np.ndarray:
        """Update mel buffer and return current mel spectrogram."""
        # Apply A-weighting filter if enabled
        if self.use_a_weighting and self.a_weighting_curve is not None:
            b, a = self.a_weighting_curve
            # Apply A-weighting filter to the audio chunk
            weighted_audio_chunk = lfilter(b, a, audio_chunk)
        else:
            weighted_audio_chunk = audio_chunk
        
        # Add to buffer
        self.mel_buffer.append(weighted_audio_chunk)
        
        # Keep only recent samples using deque's efficient operations
        total_samples = sum(len(chunk) for chunk in self.mel_buffer)
        while total_samples > self.mel_window_samples and len(self.mel_buffer) > 1:
            removed_chunk = self.mel_buffer.popleft()  # O(1) operation
            total_samples -= len(removed_chunk)
        
        # Concatenate buffer for mel analysis
        if self.mel_buffer:
            analysis_audio = np.concatenate(list(self.mel_buffer))
            if len(analysis_audio) >= self.hop_length:
                self.mel_buffer_filled = True
                return AudioUtils.compute_mel_spectrogram(
                    analysis_audio, self.sample_rate, self.n_mels, 
                    self.n_fft, self.hop_length
                )
        
        return np.array([])
    
    def _calculate_mel_gain(self, mel_spec: np.ndarray) -> float:
        """Calculate gain based on mel spectrogram analysis."""
        if mel_spec.size == 0:
            return self.min_gain_db
        
        # Calculate mel energy
        mel_energy = np.mean(mel_spec)
        
        # Convert to dB
        mel_energy_db = AudioUtils.rms_to_db(np.sqrt(mel_energy))
        
        if mel_energy_db < self.noise_gate_db:
            return self.min_gain_db
        
        # Calculate desired gain
        desired_gain_db = self.target_level_db - mel_energy_db
        
        # Clamp to allowed range
        return np.clip(desired_gain_db, self.min_gain_db, self.max_gain_db)
    
    def _smooth_gain_transition(self, desired_gain_db: float) -> float:
        """Apply smooth gain transition using attack/release time constants."""
        if desired_gain_db > self.current_gain_db:
            alpha = self.attack_alpha
        else:
            alpha = self.release_alpha
        
        self.current_gain_db = alpha * self.current_gain_db + (1.0 - alpha) * desired_gain_db
        return self.current_gain_db
    
    def update_gain(self, audio_chunk: np.ndarray) -> float:
        """
        Update AGC gain based on audio chunk without applying it.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            
        Returns:
            Current gain in dB
        """
        if not isinstance(audio_chunk, np.ndarray):
            raise ValueError("Input must be a numpy array")
        
        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32)
        
        if len(audio_chunk) == 0:
            return self.current_gain_db
        
        # Update mel analysis
        mel_spec = self._update_mel_buffer(audio_chunk)
        
        # Calculate gain based on mel spectrum
        desired_gain_db = self._calculate_mel_gain(mel_spec)
        
        # Apply smooth gain transition
        smoothed_gain_db = self._smooth_gain_transition(desired_gain_db)
        
        return smoothed_gain_db
    
    def apply_gain(self, audio_chunk: np.ndarray, gain_db: Optional[float] = None) -> np.ndarray:
        """
        Apply gain to audio chunk.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            gain_db: Gain to apply in dB (if None, uses current gain)
            
        Returns:
            Processed audio chunk with same shape and dtype as input
        """
        if not isinstance(audio_chunk, np.ndarray):
            raise ValueError("Input must be a numpy array")
        
        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32)
        
        if len(audio_chunk) == 0:
            return audio_chunk.copy()
        
        # Use provided gain or current gain
        if gain_db is None:
            gain_db = self.current_gain_db
        
        # Convert gain to linear scale and apply
        gain_linear = AudioUtils.db_to_linear(gain_db)
        processed_audio = audio_chunk * gain_linear
        
        # Prevent clipping
        max_val = np.max(np.abs(processed_audio))
        if max_val > 1.0:
            processed_audio = processed_audio / max_val
            logger.debug(f"Audio clipped, normalized by factor {max_val:.3f}")
        
        return processed_audio
    
    def process(self, audio_chunk: np.ndarray) -> np.ndarray:
        """
        Process a single audio chunk with mel-spectrum AGC.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            
        Returns:
            Processed audio chunk with same shape and dtype as input
        """
        # Update gain based on audio content
        self.update_gain(audio_chunk)
        
        # Apply current gain
        return self.apply_gain(audio_chunk)
    
    def reset(self) -> None:
        """Reset the AGC state for a new audio stream."""
        self.current_gain_db = 0.0
        self.mel_buffer.clear()  # deque.clear() is O(1)
        self.mel_buffer_filled = False
        logger.debug("MelSpectrumAGC state reset")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current AGC state information."""
        return {
            'current_gain_db': self.current_gain_db,
            'target_level_db': self.target_level_db,
            'mel_buffer_filled': self.mel_buffer_filled,
            'buffer_length': len(self.mel_buffer)
        }


class RMSAGC:
    """
    Traditional RMS-based Automatic Gain Control.
    
    This class implements a streaming AGC that adapts to varying input levels
    while maintaining consistent output levels. It supports fixed-length audio
    chunks and preserves the input/output shape consistency.
    
    Features:
    - Streaming processing with state preservation
    - Configurable target level and time constants
    - Smooth gain transitions to avoid artifacts
    - Input validation and error handling
    - A-weighting support for perceptual accuracy
    """
    
    def __init__(
        self,
        target_level_db: float = -20.0,
        max_gain_db: float = 20.0,
        min_gain_db: float = -20.0,
        attack_time_ms: float = 10.0,
        release_time_ms: float = 100.0,
        sample_rate: int = 16000,
        rms_window_ms: float = 100.0,
        noise_gate_db: float = -40.0,
        use_a_weighting: bool = True
    ):
        """
        Initialize the RMS-based AGC.
        
        Args:
            target_level_db: Target RMS level in dB (default: -20 dB)
            max_gain_db: Maximum gain in dB (default: 20 dB)
            min_gain_db: Minimum gain in dB (default: -20 dB)
            attack_time_ms: Attack time in milliseconds (default: 10 ms)
            release_time_ms: Release time in milliseconds (default: 100 ms)
            sample_rate: Audio sample rate in Hz (default: 16000)
            rms_window_ms: RMS calculation window in milliseconds (default: 100 ms)
            noise_gate_db: Noise gate threshold in dB (default: -40 dB)
            use_a_weighting: Whether to use A-weighting (default: True)
        """
        self.target_level_db = target_level_db
        self.target_level_linear = AudioUtils.db_to_linear(target_level_db)
        self.max_gain_db = max_gain_db
        self.min_gain_db = min_gain_db
        self.sample_rate = sample_rate
        self.noise_gate_db = noise_gate_db
        self.noise_gate_linear = AudioUtils.db_to_linear(noise_gate_db)
        
        # Calculate time constants
        self.attack_alpha = self._calculate_alpha(attack_time_ms)
        self.release_alpha = self._calculate_alpha(release_time_ms)
        
        # RMS calculation parameters
        self.rms_window_samples = int(rms_window_ms * sample_rate / 1000.0)
        
        # A-weighting setup
        self.use_a_weighting = use_a_weighting
        self.a_weighting_curve = None
        if use_a_weighting:
            self.a_weighting_curve = AudioUtils.get_a_weighting_curve(sample_rate)
        
        # State variables for streaming
        self.current_gain_db = 0.0
        self.rms_buffer = np.zeros(self.rms_window_samples, dtype=np.float32)
        self.rms_buffer_index = 0
        self.rms_buffer_filled = False
        
        logger.debug(f"RMSAGC initialized: target={target_level_db}dB, "
                   f"gain_range=[{min_gain_db}, {max_gain_db}]dB, "
                   f"attack={attack_time_ms}ms, release={release_time_ms}ms")
    
    def warmup(self) -> None:
        """Warmup the AGC to avoid first-time loading costs affecting performance measurements."""
        logger.debug("RMSAGC warmup started...")
        
        # Create dummy audio for warmup
        dummy_audio = np.random.randn(self.rms_window_samples).astype(np.float32)
        
        # Warmup A-weighting filter if enabled
        if self.use_a_weighting and self.a_weighting_curve is not None:
            try:
                b, a = self.a_weighting_curve
                _ = lfilter(b, a, dummy_audio)
                logger.debug("A-weighting filter warmup completed")
            except Exception as e:
                logger.warning(f"A-weighting filter warmup failed: {e}")
        
        # Warmup RMS calculation
        try:
            _ = AudioUtils.get_rms(dummy_audio, self.a_weighting_curve)
            logger.debug("RMS calculation warmup completed")
        except Exception as e:
            logger.warning(f"RMS calculation warmup failed: {e}")
        
        logger.debug("RMSAGC warmup completed successfully")
    
    def _calculate_alpha(self, time_ms: float) -> float:
        """Calculate alpha coefficient for exponential smoothing."""
        if time_ms <= 0:
            return 1.0
        return np.exp(-1.0 / (time_ms * self.sample_rate / 1000.0))
    
    def _update_rms_buffer(self, audio_chunk: np.ndarray) -> float:
        """
        Update RMS buffer and calculate current RMS level.
        
        Args:
            audio_chunk: Input audio chunk
            
        Returns:
            Current RMS level (linear scale)
        """
        chunk_size = len(audio_chunk)
        
        # Apply A-weighting filter if enabled
        if self.use_a_weighting and self.a_weighting_curve is not None:
            b, a = self.a_weighting_curve
            # Apply A-weighting filter to the audio chunk
            weighted_audio = lfilter(b, a, audio_chunk)
        else:
            weighted_audio = audio_chunk
        
        # Update circular buffer with weighted audio
        for i in range(chunk_size):
            self.rms_buffer[self.rms_buffer_index] = weighted_audio[i] ** 2
            self.rms_buffer_index = (self.rms_buffer_index + 1) % self.rms_window_samples
            
            if not self.rms_buffer_filled and self.rms_buffer_index == 0:
                self.rms_buffer_filled = True
        
        # Calculate RMS from buffer
        if self.rms_buffer_filled:
            rms_squared = np.mean(self.rms_buffer)
        else:
            # Use partial buffer if not filled yet
            valid_samples = self.rms_buffer_index if self.rms_buffer_index > 0 else self.rms_window_samples
            rms_squared = np.mean(self.rms_buffer[:valid_samples])
        
        return np.sqrt(max(rms_squared, 1e-10))  # Avoid division by zero
    
    def _calculate_desired_gain(self, current_rms: float) -> float:
        """
        Calculate desired gain based on current RMS level.
        
        Args:
            current_rms: Current RMS level (linear scale)
            
        Returns:
            Desired gain in dB
        """
        if current_rms < self.noise_gate_linear:
            # Below noise gate, use minimum gain
            return self.min_gain_db
        
        # Calculate gain needed to reach target level
        desired_gain_db = 20.0 * np.log10(self.target_level_linear / current_rms)
        
        # Clamp to allowed range
        return np.clip(desired_gain_db, self.min_gain_db, self.max_gain_db)
    
    def _smooth_gain_transition(self, desired_gain_db: float) -> float:
        """
        Apply smooth gain transition using attack/release time constants.
        
        Args:
            desired_gain_db: Desired gain in dB
            
        Returns:
            Smoothed gain in dB
        """
        if desired_gain_db > self.current_gain_db:
            # Attack: fast response to increasing levels
            alpha = self.attack_alpha
        else:
            # Release: slower response to decreasing levels
            alpha = self.release_alpha
        
        # Exponential smoothing
        self.current_gain_db = alpha * self.current_gain_db + (1.0 - alpha) * desired_gain_db
        
        return self.current_gain_db
    
    def update_gain(self, audio_chunk: np.ndarray) -> float:
        """
        Update AGC gain based on audio chunk without applying it.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            
        Returns:
            Current gain in dB
        """
        if not isinstance(audio_chunk, np.ndarray):
            raise ValueError("Input must be a numpy array")
        
        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32)
        
        if len(audio_chunk) == 0:
            return self.current_gain_db
        
        # Update RMS calculation
        current_rms = self._update_rms_buffer(audio_chunk)
        
        # Calculate desired gain
        desired_gain_db = self._calculate_desired_gain(current_rms)
        
        # Apply smooth gain transition
        smoothed_gain_db = self._smooth_gain_transition(desired_gain_db)
        
        return smoothed_gain_db
    
    def apply_gain(self, audio_chunk: np.ndarray, gain_db: Optional[float] = None) -> np.ndarray:
        """
        Apply gain to audio chunk.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            gain_db: Gain to apply in dB (if None, uses current gain)
            
        Returns:
            Processed audio chunk with same shape and dtype as input
        """
        if not isinstance(audio_chunk, np.ndarray):
            raise ValueError("Input must be a numpy array")
        
        if audio_chunk.dtype != np.float32:
            audio_chunk = audio_chunk.astype(np.float32)
        
        if len(audio_chunk) == 0:
            return audio_chunk.copy()
        
        # Use provided gain or current gain
        if gain_db is None:
            gain_db = self.current_gain_db
        
        # Convert gain to linear scale and apply
        gain_linear = AudioUtils.db_to_linear(gain_db)
        processed_audio = audio_chunk * gain_linear
        
        # Prevent clipping
        max_val = np.max(np.abs(processed_audio))
        if max_val > 1.0:
            processed_audio = processed_audio / max_val
            logger.debug(f"Audio clipped, normalized by factor {max_val:.3f}")
        
        return processed_audio
    
    def process(self, audio_chunk: np.ndarray) -> np.ndarray:
        """
        Process a single audio chunk with automatic gain control.
        
        Args:
            audio_chunk: Input audio chunk as numpy array (float32, shape: (samples,))
            
        Returns:
            Processed audio chunk with same shape and dtype as input
            
        Raises:
            ValueError: If input is invalid
        """
        # Update gain based on audio content
        self.update_gain(audio_chunk)
        
        # Apply current gain
        return self.apply_gain(audio_chunk)
    
    def reset(self) -> None:
        """Reset the AGC state for a new audio stream."""
        self.current_gain_db = 0.0
        self.rms_buffer.fill(0.0)
        self.rms_buffer_index = 0
        self.rms_buffer_filled = False
        logger.debug("RMSAGC state reset")
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current AGC state information.
        
        Returns:
            Dictionary containing current state
        """
        return {
            'current_gain_db': self.current_gain_db,
            'target_level_db': self.target_level_db,
            'rms_buffer_filled': self.rms_buffer_filled,
            'rms_buffer_index': self.rms_buffer_index
        }
    
    def set_target_level(self, target_level_db: float) -> None:
        """
        Update the target level.
        
        Args:
            target_level_db: New target level in dB
        """
        self.target_level_db = target_level_db
        self.target_level_linear = AudioUtils.db_to_linear(target_level_db)
        logger.debug(f"Target level updated to {target_level_db} dB")


class AutoGainControl:
    """
    Unified Automatic Gain Control interface.
    
    This class provides a unified interface for both RMS-based and Mel-spectrum
    AGC implementations, allowing easy switching between different algorithms.
    
    Features:
    - Support for both RMS and Mel-spectrum AGC
    - Streaming processing with state preservation
    - Configurable parameters for different use cases
    - Consistent interface regardless of underlying algorithm
    """
    
    def __init__(
        self,
        target_level_db: float = -20.0,
        max_gain_db: float = 20.0,
        min_gain_db: float = -20.0,
        attack_time_ms: float = 10.0,
        release_time_ms: float = 100.0,
        sample_rate: int = 16000,
        rms_window_ms: float = 100.0,
        noise_gate_db: float = -40.0,
        use_a_weighting: bool = True,
        agc_type: str = "rms"  # "rms" or "mel"
    ):
        """
        Initialize the Auto Gain Control.
        
        Args:
            target_level_db: Target RMS level in dB (default: -20 dB)
            max_gain_db: Maximum gain in dB (default: 20 dB)
            min_gain_db: Minimum gain in dB (default: -20 dB)
            attack_time_ms: Attack time in milliseconds (default: 10 ms)
            release_time_ms: Release time in milliseconds (default: 100 ms)
            sample_rate: Audio sample rate in Hz (default: 16000)
            rms_window_ms: RMS calculation window in milliseconds (default: 100 ms)
            noise_gate_db: Noise gate threshold in dB (default: -40 dB)
            use_a_weighting: Whether to use A-weighting (default: True)
            agc_type: AGC type - "rms" or "mel" (default: "rms")
        """
        self.agc_type = agc_type
        
        if agc_type == "mel":
            # Use mel-spectrum AGC
            self.agc_impl = MelSpectrumAGC(
                target_level_db=target_level_db,
                max_gain_db=max_gain_db,
                min_gain_db=min_gain_db,
                attack_time_ms=attack_time_ms,
                release_time_ms=release_time_ms,
                sample_rate=sample_rate,
                use_a_weighting=use_a_weighting,
                noise_gate_db=noise_gate_db
            )
        else:
            # Use traditional RMS-based AGC
            self.agc_impl = RMSAGC(
                target_level_db=target_level_db,
                max_gain_db=max_gain_db,
                min_gain_db=min_gain_db,
                attack_time_ms=attack_time_ms,
                release_time_ms=release_time_ms,
                sample_rate=sample_rate,
                rms_window_ms=rms_window_ms,
                noise_gate_db=noise_gate_db,
                use_a_weighting=use_a_weighting
            )
        
        logger.debug(f"AutoGainControl initialized: type={agc_type}, target={target_level_db}dB")
    
    def warmup(self) -> None:
        """Warmup the AGC to avoid first-time loading costs affecting performance measurements."""
        logger.debug(f"AutoGainControl warmup started for {self.agc_type} AGC...")
        self.agc_impl.warmup()
        logger.debug("AutoGainControl warmup completed")
    
    def update_gain(self, audio_chunk: np.ndarray) -> float:
        """
        Update AGC gain based on audio chunk without applying it.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            
        Returns:
            Current gain in dB
        """
        return self.agc_impl.update_gain(audio_chunk)
    
    def apply_gain(self, audio_chunk: np.ndarray, gain_db: Optional[float] = None) -> np.ndarray:
        """
        Apply gain to audio chunk.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            gain_db: Gain to apply in dB (if None, uses current gain)
            
        Returns:
            Processed audio chunk with same shape and dtype as input
        """
        return self.agc_impl.apply_gain(audio_chunk, gain_db)
    
    def process(self, audio_chunk: np.ndarray) -> np.ndarray:
        """
        Process a single audio chunk with automatic gain control.
        
        Args:
            audio_chunk: Input audio chunk as numpy array
            
        Returns:
            Processed audio chunk with same shape and dtype as input
        """
        return self.agc_impl.process(audio_chunk)
    
    def reset(self) -> None:
        """Reset the AGC state for a new audio stream."""
        self.agc_impl.reset()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current AGC state information."""
        state = self.agc_impl.get_state()
        state['agc_type'] = self.agc_type
        return state
    
    def set_target_level(self, target_level_db: float) -> None:
        """Update the target level."""
        if hasattr(self.agc_impl, 'set_target_level'):
            self.agc_impl.set_target_level(target_level_db)
        else:
            self.agc_impl.target_level_db = target_level_db
            self.agc_impl.target_level_linear = AudioUtils.db_to_linear(target_level_db)


# Factory functions for easy creation
def create_rms_agc(
    target_level_db: float = -20.0,
    max_gain_db: float = 20.0,
    min_gain_db: float = -20.0,
    attack_time_ms: float = 10.0,
    release_time_ms: float = 100.0,
    sample_rate: int = 16000,
    rms_window_ms: float = 100.0,
    noise_gate_db: float = -40.0,
    use_a_weighting: bool = True
) -> AutoGainControl:
    """
    Factory function to create an RMS-based AGC instance.
    
    Args:
        target_level_db: Target RMS level in dB
        max_gain_db: Maximum gain in dB
        min_gain_db: Minimum gain in dB
        attack_time_ms: Attack time in milliseconds
        release_time_ms: Release time in milliseconds
        sample_rate: Audio sample rate in Hz
        rms_window_ms: RMS calculation window in milliseconds
        noise_gate_db: Noise gate threshold in dB
        use_a_weighting: Whether to use A-weighting
        
    Returns:
        Configured AutoGainControl instance with RMS AGC
    """
    return AutoGainControl(
        target_level_db=target_level_db,
        max_gain_db=max_gain_db,
        min_gain_db=min_gain_db,
        attack_time_ms=attack_time_ms,
        release_time_ms=release_time_ms,
        sample_rate=sample_rate,
        rms_window_ms=rms_window_ms,
        noise_gate_db=noise_gate_db,
        use_a_weighting=use_a_weighting,
        agc_type="rms"
    )


def create_mel_agc(
    target_level_db: float = -20.0,
    max_gain_db: float = 20.0,
    min_gain_db: float = -20.0,
    attack_time_ms: float = 10.0,
    release_time_ms: float = 100.0,
    sample_rate: int = 16000,
    n_mels: int = 80,
    n_fft: int = 1024,
    hop_length: int = 256,
    mel_window_ms: float = 100.0,
    noise_gate_db: float = -40.0,
    use_a_weighting: bool = True
) -> AutoGainControl:
    """
    Factory function to create a Mel-spectrum AGC instance.
    
    Args:
        target_level_db: Target level in dB
        max_gain_db: Maximum gain in dB
        min_gain_db: Minimum gain in dB
        attack_time_ms: Attack time in milliseconds
        release_time_ms: Release time in milliseconds
        sample_rate: Audio sample rate in Hz
        n_mels: Number of mel bins
        n_fft: FFT size
        hop_length: Hop length for STFT
        mel_window_ms: Mel analysis window in milliseconds
        noise_gate_db: Noise gate threshold in dB
        use_a_weighting: Whether to use A-weighting
        
    Returns:
        Configured AutoGainControl instance with Mel-spectrum AGC
    """
    agc = AutoGainControl(
        target_level_db=target_level_db,
        max_gain_db=max_gain_db,
        min_gain_db=min_gain_db,
        attack_time_ms=attack_time_ms,
        release_time_ms=release_time_ms,
        sample_rate=sample_rate,
        noise_gate_db=noise_gate_db,
        use_a_weighting=use_a_weighting,
        agc_type="mel"
    )
    
    # Update mel-specific parameters
    if hasattr(agc.agc_impl, 'n_mels'):
        agc.agc_impl.n_mels = n_mels
    if hasattr(agc.agc_impl, 'n_fft'):
        agc.agc_impl.n_fft = n_fft
    if hasattr(agc.agc_impl, 'hop_length'):
        agc.agc_impl.hop_length = hop_length
    if hasattr(agc.agc_impl, 'mel_window_samples'):
        agc.agc_impl.mel_window_samples = int(mel_window_ms * sample_rate / 1000.0)
    
    return agc


# Legacy function for backward compatibility
def create_agc(
    target_level_db: float = -10.0,
    max_gain_db: float = 30.0,
    min_gain_db: float = -30.0,
    attack_time_ms: float = 10.0,
    release_time_ms: float = 100.0,
    sample_rate: int = 16000,
    rms_window_ms: float = 100.0,
    noise_gate_db: float = -40.0
) -> AutoGainControl:
    """
    Legacy factory function to create an AutoGainControl instance.
    
    Args:
        target_level_db: Target RMS level in dB
        max_gain_db: Maximum gain in dB
        min_gain_db: Minimum gain in dB
        attack_time_ms: Attack time in milliseconds
        release_time_ms: Release time in milliseconds
        sample_rate: Audio sample rate in Hz
        rms_window_ms: RMS calculation window in milliseconds
        noise_gate_db: Noise gate threshold in dB
        
    Returns:
        Configured AutoGainControl instance
    """
    return create_rms_agc(
        target_level_db=target_level_db,
        max_gain_db=max_gain_db,
        min_gain_db=min_gain_db,
        attack_time_ms=attack_time_ms,
        release_time_ms=release_time_ms,
        sample_rate=sample_rate,
        rms_window_ms=rms_window_ms,
        noise_gate_db=noise_gate_db
    )


# Example usage and testing functions
def example_usage():
    """Example usage of the AutoGainControl classes with visualization."""
    import numpy as np
    
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
        HAS_MATPLOTLIB = True
    except ImportError:
        print("Warning: matplotlib not available. Running without visualization.")
        HAS_MATPLOTLIB = False
    
    # Create RMS-based AGC instance
    rms_agc = create_rms_agc(
        target_level_db=-5.0,
        max_gain_db=30.0,
        min_gain_db=-30.0,
        attack_time_ms=5.0,
        release_time_ms=50.0,
        sample_rate=16000
    )
    
    # Create Mel-spectrum AGC instance
    mel_agc = create_mel_agc(
        target_level_db=-5.0,
        max_gain_db=30.0,
        min_gain_db=-30.0,
        attack_time_ms=5.0,
        release_time_ms=50.0,
        sample_rate=16000,
        n_mels=80,
        n_fft=1024,
        hop_length=256
    )
    
    # Simulate streaming audio processing with visualization
    chunk_size = 1024  # 64ms at 16kHz
    num_chunks = 200
    sample_rate = 16000
    
    # Store data for visualization
    all_input_audio = []
    all_rms_output_audio = []
    all_mel_output_audio = []
    rms_gains = []
    mel_gains = []
    time_axis = []
    
    print("Processing audio with AGC...")
    print("Testing scenarios important for speech recognition:")
    print("- Quiet speech amplification")
    print("- Small signal enhancement") 
    print("- Noise floor management")
    print("- Algorithm efficiency comparison")
    print()
    
    # Warmup AGCs to avoid first-time loading costs affecting performance measurements
    print("Warming up AGC algorithms...")
    rms_agc.warmup()
    mel_agc.warmup()
    print("Warmup completed.\n")
    
    # Timing statistics
    import time
    rms_processing_times = []
    mel_processing_times = []
    total_audio_duration = 0.0
    
    for agc_name, agc in [("RMS", rms_agc), ("Mel", mel_agc)]:
        print(f"\nTesting {agc_name} AGC:")
        agc.reset()
        
        for i in range(num_chunks):
            # Generate test audio with varying amplitude (simulating speech scenarios)
            if i < 30:  # Very quiet speech (whisper level)
                amplitude = 0.01 + 0.02 * np.sin(2 * np.pi * i / 8)  # Very low amplitude
                speech_type = "whisper"
            elif i < 60:  # Quiet speech (distant microphone)
                amplitude = 0.05 + 0.1 * np.sin(2 * np.pi * i / 10)
                speech_type = "quiet"
            elif i < 90:  # Normal speech
                amplitude = 0.3 + 0.4 * np.sin(2 * np.pi * i / 20)
                speech_type = "normal"
            elif i < 120:  # Loud speech
                amplitude = 0.8 + 0.2 * np.sin(2 * np.pi * i / 15)
                speech_type = "loud"
            elif i < 150:  # Very quiet speech again (testing AGC adaptation)
                amplitude = 0.02 + 0.03 * np.sin(2 * np.pi * i / 12)
                speech_type = "whisper"
            else:  # Mixed levels (realistic scenario)
                amplitude = 0.1 + 0.3 * np.sin(2 * np.pi * i / 25)
                speech_type = "mixed"
            
            # Add realistic noise floor
            noise_level = 0.005  # Very low noise floor
            audio_chunk = amplitude * np.random.randn(chunk_size).astype(np.float32) + noise_level * np.random.randn(chunk_size).astype(np.float32)
            
            # Process with AGC and measure timing
            start_time = time.perf_counter()
            processed_chunk = agc.process(audio_chunk)
            end_time = time.perf_counter()
            
            processing_time = end_time - start_time
            chunk_duration = len(audio_chunk) / sample_rate  # Audio duration in seconds
            total_audio_duration += chunk_duration
            
            # Store timing data
            if agc_name == "RMS":
                rms_processing_times.append(processing_time)
            else:
                mel_processing_times.append(processing_time)
            
            # Store for visualization
            if i == 0:
                all_input_audio = audio_chunk.copy()
                if agc_name == "RMS":
                    all_rms_output_audio = processed_chunk.copy()
                else:
                    all_mel_output_audio = processed_chunk.copy()
            else:
                all_input_audio = np.concatenate([all_input_audio, audio_chunk])
                if agc_name == "RMS":
                    all_rms_output_audio = np.concatenate([all_rms_output_audio, processed_chunk])
                else:
                    all_mel_output_audio = np.concatenate([all_mel_output_audio, processed_chunk])
            
            # Store gain values
            state = agc.get_state()
            if agc_name == "RMS":
                rms_gains.append(state['current_gain_db'])
            else:
                mel_gains.append(state['current_gain_db'])
            
            # Check output shape consistency
            assert processed_chunk.shape == audio_chunk.shape
            assert processed_chunk.dtype == audio_chunk.dtype
            
            if i % 40 == 0:
                rms_input = np.sqrt(np.mean(audio_chunk ** 2))
                rms_output = np.sqrt(np.mean(processed_chunk ** 2))
                snr_input = 20 * np.log10(rms_input / noise_level) if noise_level > 0 else float('inf')
                snr_output = 20 * np.log10(rms_output / noise_level) if noise_level > 0 else float('inf')
                rtf = processing_time / chunk_duration if chunk_duration > 0 else 0
                print(f"Chunk {i} ({speech_type}): Input RMS={rms_input:.4f}, Output RMS={rms_output:.4f}, "
                      f"Gain={state['current_gain_db']:.2f}dB, SNR: {snr_input:.1f}→{snr_output:.1f}dB, "
                      f"Time={processing_time*1000:.2f}ms, RTF={rtf:.3f}")
    
    # Create time axis
    time_axis = np.arange(len(all_input_audio)) / sample_rate
    
    # Calculate statistics (always needed)
    input_rms_avg = np.sqrt(np.mean(all_input_audio ** 2))
    rms_agc_rms_avg = np.sqrt(np.mean(all_rms_output_audio ** 2))
    mel_agc_rms_avg = np.sqrt(np.mean(all_mel_output_audio ** 2))
    
    # Calculate window size for dynamic range calculation
    window_size = int(0.1 * sample_rate)  # 100ms windows
    
    # Create visualization (only if matplotlib is available)
    if HAS_MATPLOTLIB:
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle('Automatic Gain Control (AGC) Comparison', fontsize=16, fontweight='bold')
        
        # Plot 1: Input audio waveform
        axes[0, 0].plot(time_axis, all_input_audio, 'b-', alpha=0.7, linewidth=0.5)
        axes[0, 0].set_title('Input Audio (Original)', fontweight='bold')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim([-1.1, 1.1])
        
        # Plot 2: RMS AGC output
        axes[0, 1].plot(time_axis, all_rms_output_audio, 'r-', alpha=0.7, linewidth=0.5)
        axes[0, 1].set_title('RMS AGC Output', fontweight='bold')
        axes[0, 1].set_ylabel('Amplitude')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim([-1.1, 1.1])
        
        # Plot 3: Mel AGC output
        axes[1, 0].plot(time_axis, all_mel_output_audio, 'g-', alpha=0.7, linewidth=0.5)
        axes[1, 0].set_title('Mel-Spectrum AGC Output', fontweight='bold')
        axes[1, 0].set_ylabel('Amplitude')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].set_ylim([-1.1, 1.1])
        
        # Plot 4: RMS comparison
        axes[1, 1].plot(time_axis, all_input_audio, 'b-', alpha=0.5, linewidth=0.5, label='Input')
        axes[1, 1].plot(time_axis, all_rms_output_audio, 'r-', alpha=0.7, linewidth=0.5, label='RMS AGC')
        axes[1, 1].set_title('Input vs RMS AGC Comparison', fontweight='bold')
        axes[1, 1].set_ylabel('Amplitude')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].set_ylim([-1.1, 1.1])
        
        # Plot 5: Gain curves
        gain_time = np.arange(len(rms_gains)) * chunk_size / sample_rate
        axes[2, 0].plot(gain_time, rms_gains, 'r-', linewidth=2, label='RMS AGC Gain')
        axes[2, 0].plot(gain_time, mel_gains, 'g-', linewidth=2, label='Mel AGC Gain')
        axes[2, 0].set_title('AGC Gain Curves', fontweight='bold')
        axes[2, 0].set_xlabel('Time (seconds)')
        axes[2, 0].set_ylabel('Gain (dB)')
        axes[2, 0].legend()
        axes[2, 0].grid(True, alpha=0.3)
        
        # Plot 6: RMS levels comparison
        # Calculate RMS in sliding windows
        rms_input = []
        rms_rms_agc = []
        rms_mel_agc = []
        rms_time = []
        
        for i in range(0, len(all_input_audio) - window_size, window_size // 2):
            rms_input.append(np.sqrt(np.mean(all_input_audio[i:i+window_size] ** 2)))
            rms_rms_agc.append(np.sqrt(np.mean(all_rms_output_audio[i:i+window_size] ** 2)))
            rms_mel_agc.append(np.sqrt(np.mean(all_mel_output_audio[i:i+window_size] ** 2)))
            rms_time.append(i / sample_rate)
        
        axes[2, 1].plot(rms_time, rms_input, 'b-', linewidth=2, label='Input RMS')
        axes[2, 1].plot(rms_time, rms_rms_agc, 'r-', linewidth=2, label='RMS AGC Output')
        axes[2, 1].plot(rms_time, rms_mel_agc, 'g-', linewidth=2, label='Mel AGC Output')
        axes[2, 1].axhline(y=10**(-20/20), color='k', linestyle='--', alpha=0.7, label='Target Level (-20dB)')
        axes[2, 1].set_title('RMS Level Comparison', fontweight='bold')
        axes[2, 1].set_xlabel('Time (seconds)')
        axes[2, 1].set_ylabel('RMS Level')
        axes[2, 1].set_yscale('log')
        axes[2, 1].legend()
        axes[2, 1].grid(True, alpha=0.3)
        
        # Add some statistics text
        stats_text = f"""Statistics:
Input RMS: {input_rms_avg:.4f}
RMS AGC Output: {rms_agc_rms_avg:.4f}
Mel AGC Output: {mel_agc_rms_avg:.4f}
RMS AGC Gain Range: {min(rms_gains):.1f} to {max(rms_gains):.1f} dB
Mel AGC Gain Range: {min(mel_gains):.1f} to {max(mel_gains):.1f} dB"""
        
        fig.text(0.02, 0.02, stats_text, fontsize=10, verticalalignment='bottom',
                 bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        plt.show()
    
    # Calculate speech recognition specific metrics
    # Analyze quiet speech segments (chunks 0-30 and 120-150)
    quiet_segments_input = []
    quiet_segments_rms_output = []
    quiet_segments_mel_output = []
    
    # Extract quiet speech segments for analysis
    quiet_chunk_indices = list(range(0, 30)) + list(range(120, 150))
    quiet_start_sample = 0
    quiet_end_sample = 0
    
    for i, chunk_idx in enumerate(quiet_chunk_indices):
        start_sample = chunk_idx * chunk_size
        end_sample = start_sample + chunk_size
        
        if i == 0:
            quiet_start_sample = start_sample
        if i == len(quiet_chunk_indices) - 1:
            quiet_end_sample = end_sample
    
    # Analyze quiet speech performance
    if quiet_end_sample > quiet_start_sample:
        quiet_input = all_input_audio[quiet_start_sample:quiet_end_sample]
        quiet_rms_output = all_rms_output_audio[quiet_start_sample:quiet_end_sample]
        quiet_mel_output = all_mel_output_audio[quiet_start_sample:quiet_end_sample]
        
        quiet_input_rms = np.sqrt(np.mean(quiet_input ** 2))
        quiet_rms_output_rms = np.sqrt(np.mean(quiet_rms_output ** 2))
        quiet_mel_output_rms = np.sqrt(np.mean(quiet_mel_output ** 2))
        
        # Calculate amplification factors for quiet speech
        rms_amplification = quiet_rms_output_rms / quiet_input_rms if quiet_input_rms > 0 else 1.0
        mel_amplification = quiet_mel_output_rms / quiet_input_rms if quiet_input_rms > 0 else 1.0
        
        # Calculate SNR improvement
        noise_floor = 0.005  # Same as in the test
        snr_input_quiet = 20 * np.log10(quiet_input_rms / noise_floor) if noise_floor > 0 else float('inf')
        snr_rms_output_quiet = 20 * np.log10(quiet_rms_output_rms / noise_floor) if noise_floor > 0 else float('inf')
        snr_mel_output_quiet = 20 * np.log10(quiet_mel_output_rms / noise_floor) if noise_floor > 0 else float('inf')
    
    # Print summary statistics
    print(f"\n=== AGC Performance Summary ===")
    print(f"Input RMS average: {input_rms_avg:.4f}")
    print(f"RMS AGC output RMS average: {rms_agc_rms_avg:.4f}")
    print(f"Mel AGC output RMS average: {mel_agc_rms_avg:.4f}")
    print(f"RMS AGC gain range: {min(rms_gains):.1f} to {max(rms_gains):.1f} dB")
    print(f"Mel AGC gain range: {min(mel_gains):.1f} to {max(mel_gains):.1f} dB")
    
    print(f"\n=== Speech Recognition Performance Analysis ===")
    if quiet_end_sample > quiet_start_sample:
        print(f"Quiet Speech Amplification:")
        print(f"  RMS AGC: {rms_amplification:.1f}x ({20*np.log10(rms_amplification):.1f} dB)")
        print(f"  Mel AGC: {mel_amplification:.1f}x ({20*np.log10(mel_amplification):.1f} dB)")
        print(f"  SNR Improvement (RMS): {snr_rms_output_quiet - snr_input_quiet:.1f} dB")
        print(f"  SNR Improvement (Mel): {snr_mel_output_quiet - snr_input_quiet:.1f} dB")
        
        # Speech recognition quality indicators
        print(f"\nSpeech Recognition Quality Indicators:")
        print(f"  Quiet speech input SNR: {snr_input_quiet:.1f} dB")
        print(f"  RMS AGC output SNR: {snr_rms_output_quiet:.1f} dB")
        print(f"  Mel AGC output SNR: {snr_mel_output_quiet:.1f} dB")
        
        # Recommended SNR for speech recognition is typically > 10 dB
        rms_snr_adequate = snr_rms_output_quiet > 10
        mel_snr_adequate = snr_mel_output_quiet > 10
        print(f"  RMS AGC adequate for ASR: {'✅ Yes' if rms_snr_adequate else '❌ No'} (need >10 dB)")
        print(f"  Mel AGC adequate for ASR: {'✅ Yes' if mel_snr_adequate else '❌ No'} (need >10 dB)")
    
    # Calculate compression ratios
    input_dynamic_range = 20 * np.log10(np.max(np.abs(all_input_audio)) / np.max([np.sqrt(np.mean(all_input_audio[i:i+window_size] ** 2)) for i in range(0, len(all_input_audio) - window_size, window_size)]))
    rms_agc_dynamic_range = 20 * np.log10(np.max(np.abs(all_rms_output_audio)) / np.max([np.sqrt(np.mean(all_rms_output_audio[i:i+window_size] ** 2)) for i in range(0, len(all_rms_output_audio) - window_size, window_size)]))
    mel_agc_dynamic_range = 20 * np.log10(np.max(np.abs(all_mel_output_audio)) / np.max([np.sqrt(np.mean(all_mel_output_audio[i:i+window_size] ** 2)) for i in range(0, len(all_mel_output_audio) - window_size, window_size)]))
    
    print(f"Input dynamic range: {input_dynamic_range:.1f} dB")
    print(f"RMS AGC dynamic range: {rms_agc_dynamic_range:.1f} dB")
    print(f"Mel AGC dynamic range: {mel_agc_dynamic_range:.1f} dB")
    print(f"RMS AGC compression ratio: {input_dynamic_range/rms_agc_dynamic_range:.1f}:1")
    print(f"Mel AGC compression ratio: {input_dynamic_range/mel_agc_dynamic_range:.1f}:1")
    
    # Calculate timing statistics
    if rms_processing_times and mel_processing_times:
        rms_total_time = sum(rms_processing_times)
        mel_total_time = sum(mel_processing_times)
        
        rms_avg_time = np.mean(rms_processing_times)
        mel_avg_time = np.mean(mel_processing_times)
        
        rms_rtf = rms_total_time / total_audio_duration if total_audio_duration > 0 else 0
        mel_rtf = mel_total_time / total_audio_duration if total_audio_duration > 0 else 0
        
        rms_max_time = np.max(rms_processing_times)
        mel_max_time = np.max(mel_processing_times)
        
        rms_min_time = np.min(rms_processing_times)
        mel_min_time = np.min(mel_processing_times)
        
        print(f"\n=== Algorithm Performance Analysis ===")
        print(f"Total audio duration: {total_audio_duration:.2f} seconds")
        print(f"Number of chunks processed: {len(rms_processing_times)}")
        print(f"Chunk size: {chunk_size} samples ({chunk_size/sample_rate*1000:.1f} ms)")
        
        print(f"\nRMS AGC Performance:")
        print(f"  Total processing time: {rms_total_time*1000:.2f} ms")
        print(f"  Average time per chunk: {rms_avg_time*1000:.2f} ms")
        print(f"  Min/Max time per chunk: {rms_min_time*1000:.2f}/{rms_max_time*1000:.2f} ms")
        print(f"  Real-Time Factor (RTF): {rms_rtf:.4f}")
        print(f"  Processing speed: {1/rms_rtf:.1f}x real-time" if rms_rtf > 0 else "  Processing speed: N/A")
        
        print(f"\nMel AGC Performance:")
        print(f"  Total processing time: {mel_total_time*1000:.2f} ms")
        print(f"  Average time per chunk: {mel_avg_time*1000:.2f} ms")
        print(f"  Min/Max time per chunk: {mel_min_time*1000:.2f}/{mel_max_time*1000:.2f} ms")
        print(f"  Real-Time Factor (RTF): {mel_rtf:.4f}")
        print(f"  Processing speed: {1/mel_rtf:.1f}x real-time" if mel_rtf > 0 else "  Processing speed: N/A")
        
        print(f"\nAlgorithm Comparison:")
        speed_ratio = rms_avg_time / mel_avg_time if mel_avg_time > 0 else float('inf')
        if speed_ratio > 1:
            print(f"  RMS AGC is {speed_ratio:.2f}x faster than Mel AGC")
        else:
            print(f"  Mel AGC is {1/speed_ratio:.2f}x faster than RMS AGC")
        
        rtf_ratio = rms_rtf / mel_rtf if mel_rtf > 0 else float('inf')
        print(f"  RTF ratio (RMS/Mel): {rtf_ratio:.3f}")
        
        # Efficiency recommendations
        print(f"\nEfficiency Recommendations:")
        if rms_rtf < 0.1:
            print(f"  ✅ RMS AGC: Excellent real-time performance (RTF < 0.1)")
        elif rms_rtf < 0.5:
            print(f"  ✅ RMS AGC: Good real-time performance (RTF < 0.5)")
        elif rms_rtf < 1.0:
            print(f"  ⚠️  RMS AGC: Acceptable real-time performance (RTF < 1.0)")
        else:
            print(f"  ❌ RMS AGC: Poor real-time performance (RTF > 1.0)")
            
        if mel_rtf < 0.1:
            print(f"  ✅ Mel AGC: Excellent real-time performance (RTF < 0.1)")
        elif mel_rtf < 0.5:
            print(f"  ✅ Mel AGC: Good real-time performance (RTF < 0.5)")
        elif mel_rtf < 1.0:
            print(f"  ⚠️  Mel AGC: Acceptable real-time performance (RTF < 1.0)")
        else:
            print(f"  ❌ Mel AGC: Poor real-time performance (RTF > 1.0)")
        
        # Memory usage estimation
        rms_memory_per_chunk = chunk_size * 4 * 2  # float32 input + output
        mel_memory_per_chunk = chunk_size * 4 * 2 + 80 * 256 * 4  # float32 + mel spectrogram
        print(f"\nMemory Usage Estimation:")
        print(f"  RMS AGC: ~{rms_memory_per_chunk/1024:.1f} KB per chunk")
        print(f"  Mel AGC: ~{mel_memory_per_chunk/1024:.1f} KB per chunk")
        print(f"  Mel overhead: {mel_memory_per_chunk/rms_memory_per_chunk:.1f}x more memory")


if __name__ == "__main__":
    # Run visualization example
    print("Running AGC visualization example...")
    print("=" * 60)
    
    # Run full visualization example
    example_usage()