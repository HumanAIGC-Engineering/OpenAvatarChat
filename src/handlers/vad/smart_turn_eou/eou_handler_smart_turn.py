import os
from abc import ABC
from typing import Dict, Optional, cast

import numpy as np
from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalType, ChatSignalSourceType
from chat_engine.data_models.internal.handler_definition_data import ChatDataConsumeMode
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from chat_engine.data_models.runtime_data.event_model import EventType


class SmartTurnEOUConfigModel(HandlerBaseConfigModel, BaseModel):
    threshold: float = Field(default=0.5, description="Probability threshold for completion detection")
    max_buffer_seconds: float = Field(default=12.0, description="Maximum buffer duration in seconds")
    sample_rate: int = Field(default=16000, description="Audio sample rate")
    model_path: str = Field(default="models/smart_turn/smart-turn-v3.1-cpu.onnx", description="Path to ONNX model")


class SmartTurnEOUContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[SmartTurnEOUConfigModel] = None
        
        # Audio buffer to accumulate segments
        self.audio_buffer = []
        self.buffer_duration = 0.0
        
        # Track current stream
        self.current_stream_id = None
        
        # Flag to track if we've sent end signal for current stream
        self.end_signal_sent = False
        
        # Model components (initialized in handler.load)
        self.session = None
        self.feature_extractor = None
        
        # Shared states
        self.shared_states = None

    def reset_buffer(self):
        """Reset the audio buffer."""
        self.audio_buffer.clear()
        self.buffer_duration = 0.0
        self.end_signal_sent = False
        self.current_stream_id = None
        logger.debug("Smart Turn EOU: Buffer reset")

    def add_to_buffer(self, audio: np.ndarray, sample_rate: int):
        """Add audio to buffer and update duration."""
        self.audio_buffer.append(audio)
        self.buffer_duration += len(audio) / sample_rate
        logger.debug(f"Smart Turn EOU: Buffer duration now {self.buffer_duration:.2f}s")

    def get_buffered_audio(self) -> Optional[np.ndarray]:
        """Get concatenated buffered audio."""
        if not self.audio_buffer:
            return None
        return np.concatenate(self.audio_buffer, axis=0)


class HandlerSmartTurnEOU(HandlerBase, ABC):
    def __init__(self):
        super().__init__()
        self.model_session = None
        self.feature_extractor = None

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="SmartTurnEOU",
            config_model=SmartTurnEOUConfigModel,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        """Load the Smart Turn ONNX model and feature extractor."""
        import onnxruntime as ort
        from transformers import WhisperFeatureExtractor
        
        config = handler_config if isinstance(handler_config, SmartTurnEOUConfigModel) else SmartTurnEOUConfigModel()
        
        # Resolve model path
        model_path = config.model_path
        if not os.path.isabs(model_path):
            from engine_utils.directory_info import DirectoryInfo
            model_path = os.path.join(DirectoryInfo.get_project_dir(), model_path)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Smart Turn model not found at {model_path}. "
                f"Please run: bash scripts/download_smart_turn_weights.sh"
            )
        
        # Build ONNX session
        so = ort.SessionOptions()
        so.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
        so.inter_op_num_threads = 1
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        so.log_severity_level = 4
        
        self.model_session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"],
            sess_options=so
        )
        
        # Initialize Whisper feature extractor
        self.feature_extractor = WhisperFeatureExtractor(chunk_length=8)
        
        logger.info(f"Smart Turn EOU model loaded from {model_path}")

    def create_context(self, session_context: SessionContext, handler_config=None) -> HandlerContext:
        """Create handler context."""
        if not isinstance(handler_config, SmartTurnEOUConfigModel):
            handler_config = SmartTurnEOUConfigModel()
        
        context = SmartTurnEOUContext(session_context.session_info.session_id)
        context.config = handler_config
        context.session = self.model_session
        context.feature_extractor = self.feature_extractor
        context.shared_states = session_context.shared_states
        
        return context

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        """Start handler context."""
        pass

    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        """Define input/output data types - 旁路监听模式，不消费也不产生数据。"""
        inputs = {
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
                input_consume_mode=ChatDataConsumeMode.DEFAULT,  # 旁路监听，不阻断数据流
                input_priority=100,  # 低优先级，不影响 ASR
            )
        }
        
        # 不输出数据，只发送信号
        return HandlerDetail(inputs=inputs, outputs={})

    def _truncate_audio_to_last_n_seconds(self, audio_array: np.ndarray, n_seconds: int = 8, sample_rate: int = 16000) -> np.ndarray:
        """Truncate audio to last n seconds or pad with zeros to meet n seconds."""
        max_samples = n_seconds * sample_rate
        if len(audio_array) > max_samples:
            return audio_array[-max_samples:]
        elif len(audio_array) < max_samples:
            # Pad with zeros at the beginning
            padding = max_samples - len(audio_array)
            return np.pad(audio_array, (padding, 0), mode='constant', constant_values=0)
        return audio_array

    def _predict_eou(self, context: SmartTurnEOUContext, audio_array: np.ndarray) -> Dict:
        """
        Predict whether the audio segment is complete (turn ended) or incomplete.
        
        Returns:
            Dictionary with 'prediction' (1=complete, 0=incomplete) and 'probability'
        """
        # Truncate to 8 seconds (keeping the end) or pad to 8 seconds
        audio_array = self._truncate_audio_to_last_n_seconds(audio_array, n_seconds=8)
        
        # Process audio using Whisper's feature extractor
        inputs = context.feature_extractor(
            audio_array,
            sampling_rate=16000,
            return_tensors="np",
            padding="max_length",
            max_length=8 * 16000,
            truncation=True,
            do_normalize=True,
        )
        
        # Extract features and ensure correct shape for ONNX
        input_features = inputs.input_features.squeeze(0).astype(np.float32)
        input_features = np.expand_dims(input_features, axis=0)  # Add batch dimension
        
        # Run ONNX inference
        outputs = context.session.run(None, {"input_features": input_features})
        
        # Extract probability (ONNX model returns sigmoid probabilities)
        probability = outputs[0][0].item()
        
        # Make prediction (1 for Complete, 0 for Incomplete)
        prediction = 1 if probability > context.config.threshold else 0
        
        return {
            "prediction": prediction,
            "probability": probability,
        }

    def handle(self, context: HandlerContext, inputs: ChatData, output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """
        Handle incoming HUMAN_AUDIO data from VAD (旁路监听模式).
        
        Logic:
        1. 累积音频数据到 buffer
        2. 检测 EVT_EARLY_VAD_END Event
        3. 如果检测到，运行 Smart Turn 模型判断
        4. 如果判断为完成，发送 candidate STREAM_END 信号给 VAD
        5. 如果判断未完成，等待下一个 early_vad_end（VAD 会持续发送）
        6. 不输出任何数据（旁路监听模式）
        """
        context = cast(SmartTurnEOUContext, context)
        
        if inputs.type != ChatDataType.HUMAN_AUDIO:
            return
        
        # Get audio data
        audio = inputs.data.get_main_data() if inputs.data else None
        if audio is None:
            return
        
        audio_entry = inputs.data.get_main_definition_entry()
        sample_rate = audio_entry.sample_rate
        audio = audio.squeeze()
        
        # Convert to float32 if needed
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32) / 32767.0
        
        # Check for new stream
        if inputs.is_first_data:
            logger.info("Smart Turn EOU: New stream detected, resetting buffer")
            context.reset_buffer()
            context.current_stream_id = inputs.stream_id
        
        # Add audio to buffer
        context.add_to_buffer(audio, sample_rate)
        
        # 检测 EVT_EARLY_VAD_END Event
        has_early_end = inputs.data.has_event(EventType.EVT_EARLY_VAD_END) if inputs.data else False
        
        if has_early_end and not context.end_signal_sent:
            # 运行 Smart Turn 模型判断
            buffered_audio = context.get_buffered_audio()
            if buffered_audio is not None and len(buffered_audio) > 0:
                result = self._predict_eou(context, buffered_audio)
                prediction = result["prediction"]
                probability = result["probability"]
                
                logger.info(
                    f"Smart Turn EOU: Prediction={prediction} "
                    f"({'Complete' if prediction == 1 else 'Incomplete'}), "
                    f"Probability={probability:.4f}, "
                    f"Buffer duration={context.buffer_duration:.2f}s"
                )
                
                if prediction == 1:
                    # 判断为完成，发送 candidate STREAM_END 信号
                    if context.current_stream_id:
                        signal = ChatSignal(
                            type=ChatSignalType.STREAM_END,
                            source_type=ChatSignalSourceType.HANDLER,
                            related_stream=context.current_stream_id,
                            signal_data={
                                "eou_prediction": prediction,
                                "eou_probability": probability,
                                "eou_buffer_duration_ms": context.buffer_duration * 1000,
                            }
                        )
                        context.emit_signal(signal)
                        context.end_signal_sent = True
                        logger.info(f"Smart Turn EOU: Sent candidate STREAM_END signal for stream {context.current_stream_id}")
                else:
                    # 判断未完成，等待下一个 early_vad_end（VAD 会持续发送）
                    logger.info("Smart Turn EOU: Utterance incomplete, waiting for next early_vad_end")
        
        # 处理真正的 stream end（由 VAD 发出的正式结束）
        if inputs.is_last_data:
            logger.info(f"Smart Turn EOU: Stream ended, buffer duration was {context.buffer_duration:.2f}s")
            context.reset_buffer()

    def destroy_context(self, context: HandlerContext):
        """Clean up context resources."""
        context = cast(SmartTurnEOUContext, context)
        context.reset_buffer()

