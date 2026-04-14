#!/usr/bin/env python3
"""
Unit tests for AGC speech recognition functionality.
"""

import unittest
import numpy as np
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from engine_utils.audio_utils.auto_gain_control import (
    create_rms_agc, 
    create_mel_agc, 
    AudioUtils
)


class TestAGCSpeechRecognition(unittest.TestCase):
    """Test AGC functionality for speech recognition scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.noise_floor = 0.001
        
        # Create AGC instances optimized for speech recognition
        self.rms_agc = create_rms_agc(
            target_level_db=-10.0,
            max_gain_db=30.0,
            min_gain_db=-30.0,
            attack_time_ms=5.0,
            release_time_ms=50.0,
            sample_rate=self.sample_rate,
            noise_gate_db=-50.0
        )
        
        self.mel_agc = create_mel_agc(
            target_level_db=-10.0,
            max_gain_db=30.0,
            min_gain_db=-30.0,
            attack_time_ms=5.0,
            release_time_ms=50.0,
            sample_rate=self.sample_rate,
            noise_gate_db=-50.0
        )
        
        # Warmup AGCs to avoid first-time loading costs affecting performance tests
        self.rms_agc.warmup()
        self.mel_agc.warmup()
    
    def test_whisper_speech_amplification(self):
        """Test AGC amplification of whisper-level speech."""
        # Very quiet speech (whisper level)
        amplitude = 0.005
        audio_chunk = amplitude * np.random.randn(self.chunk_size).astype(np.float32) + self.noise_floor * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Process with both AGCs
        self.rms_agc.reset()
        self.mel_agc.reset()
        
        rms_output = self.rms_agc.process(audio_chunk)
        mel_output = self.mel_agc.process(audio_chunk)
        
        # Calculate metrics
        input_rms = np.sqrt(np.mean(audio_chunk ** 2))
        rms_output_rms = np.sqrt(np.mean(rms_output ** 2))
        mel_output_rms = np.sqrt(np.mean(mel_output ** 2))
        
        # Should amplify quiet speech significantly
        rms_amplification = rms_output_rms / input_rms if input_rms > 0 else 1.0
        mel_amplification = mel_output_rms / input_rms if input_rms > 0 else 1.0
        
        # Check amplification (should be > 10x for whisper)
        self.assertGreater(rms_amplification, 10.0, "RMS AGC should amplify whisper speech >10x")
        self.assertGreater(mel_amplification, 10.0, "Mel AGC should amplify whisper speech >10x")
        
        # Check output SNR (should be > 10 dB for good ASR)
        rms_snr = 20 * np.log10(rms_output_rms / self.noise_floor) if self.noise_floor > 0 else float('inf')
        mel_snr = 20 * np.log10(mel_output_rms / self.noise_floor) if self.noise_floor > 0 else float('inf')
        
        self.assertGreater(rms_snr, 10.0, "RMS AGC output SNR should be >10 dB for ASR")
        self.assertGreater(mel_snr, 10.0, "Mel AGC output SNR should be >10 dB for ASR")
    
    def test_quiet_speech_amplification(self):
        """Test AGC amplification of quiet speech."""
        # Quiet speech (distant microphone)
        amplitude = 0.02
        audio_chunk = amplitude * np.random.randn(self.chunk_size).astype(np.float32) + self.noise_floor * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Process with both AGCs
        self.rms_agc.reset()
        self.mel_agc.reset()
        
        rms_output = self.rms_agc.process(audio_chunk)
        mel_output = self.mel_agc.process(audio_chunk)
        
        # Calculate metrics
        input_rms = np.sqrt(np.mean(audio_chunk ** 2))
        rms_output_rms = np.sqrt(np.mean(rms_output ** 2))
        mel_output_rms = np.sqrt(np.mean(mel_output ** 2))
        
        # Should amplify quiet speech
        rms_amplification = rms_output_rms / input_rms if input_rms > 0 else 1.0
        mel_amplification = mel_output_rms / input_rms if input_rms > 0 else 1.0
        
        # Check amplification (should be > 2x for quiet speech)
        self.assertGreater(rms_amplification, 2.0, "RMS AGC should amplify quiet speech >2x")
        self.assertGreater(mel_amplification, 2.0, "Mel AGC should amplify quiet speech >2x")
    
    def test_normal_speech_processing(self):
        """Test AGC processing of normal speech levels."""
        # Normal speech
        amplitude = 0.1
        audio_chunk = amplitude * np.random.randn(self.chunk_size).astype(np.float32) + self.noise_floor * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Process with both AGCs
        self.rms_agc.reset()
        self.mel_agc.reset()
        
        rms_output = self.rms_agc.process(audio_chunk)
        mel_output = self.mel_agc.process(audio_chunk)
        
        # Calculate metrics
        input_rms = np.sqrt(np.mean(audio_chunk ** 2))
        rms_output_rms = np.sqrt(np.mean(rms_output ** 2))
        mel_output_rms = np.sqrt(np.mean(mel_output ** 2))
        
        # Should maintain or slightly adjust normal speech
        rms_gain = 20 * np.log10(rms_output_rms / input_rms) if input_rms > 0 else 0
        mel_gain = 20 * np.log10(mel_output_rms / input_rms) if input_rms > 0 else 0
        
        # Gain should be reasonable (within ±10 dB)
        self.assertLess(abs(rms_gain), 10.0, "RMS AGC gain should be within ±10 dB for normal speech")
        self.assertLess(abs(mel_gain), 10.0, "Mel AGC gain should be within ±10 dB for normal speech")
    
    def test_loud_speech_attenuation(self):
        """Test AGC attenuation of loud speech."""
        # Loud speech
        amplitude = 0.5
        audio_chunk = amplitude * np.random.randn(self.chunk_size).astype(np.float32) + self.noise_floor * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Process with both AGCs
        self.rms_agc.reset()
        self.mel_agc.reset()
        
        rms_output = self.rms_agc.process(audio_chunk)
        mel_output = self.mel_agc.process(audio_chunk)
        
        # Calculate metrics
        input_rms = np.sqrt(np.mean(audio_chunk ** 2))
        rms_output_rms = np.sqrt(np.mean(rms_output ** 2))
        mel_output_rms = np.sqrt(np.mean(mel_output ** 2))
        
        # Should attenuate loud speech
        rms_gain = 20 * np.log10(rms_output_rms / input_rms) if input_rms > 0 else 0
        mel_gain = 20 * np.log10(mel_output_rms / input_rms) if input_rms > 0 else 0
        
        # Should have negative gain (attenuation)
        self.assertLess(rms_gain, 0.0, "RMS AGC should attenuate loud speech")
        self.assertLess(mel_gain, 0.0, "Mel AGC should attenuate loud speech")
    
    def test_clipping_protection(self):
        """Test AGC clipping protection for very loud input."""
        # Very loud speech that would cause clipping
        amplitude = 2.0  # Very loud
        audio_chunk = amplitude * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Process with AGC
        self.rms_agc.reset()
        rms_output = self.rms_agc.process(audio_chunk)
        
        # Check for clipping protection
        max_output = np.max(np.abs(rms_output))
        self.assertLessEqual(max_output, 1.0, "AGC should prevent clipping (max output ≤ 1.0)")
    
    def test_empty_chunk_handling(self):
        """Test AGC handling of empty audio chunks."""
        empty_chunk = np.array([], dtype=np.float32)
        
        # Process empty chunk
        self.rms_agc.reset()
        rms_output = self.rms_agc.process(empty_chunk)
        
        # Should return empty chunk with same shape
        self.assertEqual(rms_output.shape, empty_chunk.shape, "Empty chunk should return empty output")
        self.assertEqual(rms_output.dtype, empty_chunk.dtype, "Output dtype should match input dtype")
    
    def test_agc_state_management(self):
        """Test AGC state management and reset functionality."""
        # Process some audio
        audio_chunk = 0.1 * np.random.randn(self.chunk_size).astype(np.float32)
        self.rms_agc.process(audio_chunk)
        
        # Get state
        state_before = self.rms_agc.get_state()
        self.assertIn('current_gain_db', state_before)
        self.assertIn('target_level_db', state_before)
        
        # Reset and check state
        self.rms_agc.reset()
        state_after = self.rms_agc.get_state()
        
        # Gain should be reset
        self.assertEqual(state_after['current_gain_db'], 0.0, "Gain should be reset to 0 dB")
    
    def test_agc_warmup_functionality(self):
        """Test AGC warmup functionality."""
        # Test that warmup doesn't raise exceptions
        try:
            self.rms_agc.warmup()
            self.mel_agc.warmup()
        except Exception as e:
            self.fail(f"AGC warmup should not raise exceptions: {e}")
        
        # Test that warmup can be called multiple times
        try:
            self.rms_agc.warmup()
            self.mel_agc.warmup()
        except Exception as e:
            self.fail(f"Multiple AGC warmup calls should not raise exceptions: {e}")
        
        # Test that AGC still works after warmup
        audio_chunk = 0.1 * np.random.randn(self.chunk_size).astype(np.float32)
        rms_output = self.rms_agc.process(audio_chunk)
        mel_output = self.mel_agc.process(audio_chunk)
        
        self.assertEqual(rms_output.shape, audio_chunk.shape)
        self.assertEqual(mel_output.shape, audio_chunk.shape)
    
    def test_separate_gain_update_and_application(self):
        """Test separate gain update and application functionality."""
        audio_chunk = 0.1 * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Test RMS AGC
        # Update gain without applying
        rms_gain = self.rms_agc.update_gain(audio_chunk)
        self.assertIsInstance(rms_gain, float)
        self.assertGreaterEqual(rms_gain, self.rms_agc.min_gain_db)
        self.assertLessEqual(rms_gain, self.rms_agc.max_gain_db)
        
        # Apply gain
        rms_output = self.rms_agc.apply_gain(audio_chunk)
        self.assertEqual(rms_output.shape, audio_chunk.shape)
        self.assertEqual(rms_output.dtype, audio_chunk.dtype)
        
        # Test with custom gain
        custom_gain = 10.0  # 10 dB
        rms_output_custom = self.rms_agc.apply_gain(audio_chunk, custom_gain)
        self.assertEqual(rms_output_custom.shape, audio_chunk.shape)
        
        # Test Mel AGC
        # Update gain without applying
        mel_gain = self.mel_agc.update_gain(audio_chunk)
        self.assertIsInstance(mel_gain, float)
        self.assertGreaterEqual(mel_gain, self.mel_agc.min_gain_db)
        self.assertLessEqual(mel_gain, self.mel_agc.max_gain_db)
        
        # Apply gain
        mel_output = self.mel_agc.apply_gain(audio_chunk)
        self.assertEqual(mel_output.shape, audio_chunk.shape)
        self.assertEqual(mel_output.dtype, audio_chunk.dtype)
        
        # Test with custom gain
        mel_output_custom = self.mel_agc.apply_gain(audio_chunk, custom_gain)
        self.assertEqual(mel_output_custom.shape, audio_chunk.shape)
    
    def test_gain_consistency(self):
        """Test that separate gain update and application gives same result as process."""
        audio_chunk = 0.1 * np.random.randn(self.chunk_size).astype(np.float32)
        
        # Test RMS AGC
        # Method 1: Separate update and apply
        self.rms_agc.reset()
        rms_gain = self.rms_agc.update_gain(audio_chunk)
        rms_output_separate = self.rms_agc.apply_gain(audio_chunk)
        
        # Method 2: Direct process
        self.rms_agc.reset()
        rms_output_process = self.rms_agc.process(audio_chunk)
        
        # Results should be the same
        np.testing.assert_array_almost_equal(rms_output_separate, rms_output_process, decimal=6)
        
        # Test Mel AGC
        # Method 1: Separate update and apply
        self.mel_agc.reset()
        mel_gain = self.mel_agc.update_gain(audio_chunk)
        mel_output_separate = self.mel_agc.apply_gain(audio_chunk)
        
        # Method 2: Direct process
        self.mel_agc.reset()
        mel_output_process = self.mel_agc.process(audio_chunk)
        
        # Results should be the same
        np.testing.assert_array_almost_equal(mel_output_separate, mel_output_process, decimal=6)
    
    def test_audio_utils_functions(self):
        """Test AudioUtils helper functions."""
        # Test RMS calculation
        test_audio = np.array([1.0, -1.0, 0.5, -0.5], dtype=np.float32)
        rms = AudioUtils.get_rms(test_audio)
        expected_rms = np.sqrt(np.mean(test_audio ** 2))
        self.assertAlmostEqual(rms, expected_rms, places=6)
        
        # Test dB conversion
        db_value = AudioUtils.rms_to_db(0.1)
        expected_db = 20 * np.log10(0.1)
        self.assertAlmostEqual(db_value, expected_db, places=6)
        
        # Test linear conversion
        linear_value = AudioUtils.db_to_linear(20.0)
        expected_linear = 10.0 ** (20.0 / 20.0)
        self.assertAlmostEqual(linear_value, expected_linear, places=6)
    
    def test_snr_improvement(self):
        """Test SNR improvement for speech recognition."""
        # Test with quiet speech and noise
        signal_amplitude = 0.01
        noise_amplitude = 0.005
        
        # Create signal + noise
        signal = signal_amplitude * np.random.randn(self.chunk_size).astype(np.float32)
        noise = noise_amplitude * np.random.randn(self.chunk_size).astype(np.float32)
        audio_chunk = signal + noise
        
        # Process with AGC
        self.rms_agc.reset()
        rms_output = self.rms_agc.process(audio_chunk)
        
        # Calculate SNR before and after
        input_snr = 20 * np.log10(signal_amplitude / noise_amplitude)
        output_signal_rms = np.sqrt(np.mean(rms_output ** 2))
        output_snr = 20 * np.log10(output_signal_rms / noise_amplitude)
        
        # SNR should improve (or at least not degrade significantly)
        snr_improvement = output_snr - input_snr
        self.assertGreaterEqual(snr_improvement, -5.0, "SNR should not degrade by more than 5 dB")


class TestAGCSpeechScenarios(unittest.TestCase):
    """Test AGC with realistic speech scenarios."""
    
    def test_speech_scenario_matrix(self):
        """Test AGC across different speech scenarios."""
        scenarios = [
            ("Whisper", 0.005, "Very quiet speech"),
            ("Quiet", 0.02, "Distant microphone"),
            ("Normal", 0.1, "Normal conversation"),
            ("Loud", 0.5, "Loud speech"),
            ("Mixed", 0.05, "Varying levels")
        ]
        
        rms_agc = create_rms_agc(
            target_level_db=-10.0,
            max_gain_db=30.0,
            min_gain_db=-30.0,
            sample_rate=16000,
            noise_gate_db=-50.0
        )
        
        results = []
        
        for scenario_name, amplitude, description in scenarios:
            # Generate test audio
            audio_chunk = amplitude * np.random.randn(1024).astype(np.float32) + 0.001 * np.random.randn(1024).astype(np.float32)
            
            # Process with AGC
            rms_agc.reset()
            rms_output = rms_agc.process(audio_chunk)
            
            # Calculate metrics
            input_rms = np.sqrt(np.mean(audio_chunk ** 2))
            output_rms = np.sqrt(np.mean(rms_output ** 2))
            gain_db = 20 * np.log10(output_rms / input_rms) if input_rms > 0 else 0
            snr = 20 * np.log10(output_rms / 0.001) if 0.001 > 0 else float('inf')
            
            results.append({
                'scenario': scenario_name,
                'input_rms': input_rms,
                'output_rms': output_rms,
                'gain_db': gain_db,
                'snr_db': snr
            })
            
            # Basic assertions
            self.assertGreater(output_rms, 0.0, f"Output RMS should be positive for {scenario_name}")
            self.assertLess(abs(gain_db), 40.0, f"Gain should be within reasonable range for {scenario_name}")
        
        # Print results for manual inspection
        print("\nSpeech Scenario Test Results:")
        print("Scenario | Input RMS | Output RMS | Gain (dB) | SNR (dB)")
        print("-" * 60)
        for result in results:
            print(f"{result['scenario']:8} | {result['input_rms']:.4f}    | {result['output_rms']:.4f}  | {result['gain_db']:6.1f}dB | {result['snr_db']:6.1f}dB")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
