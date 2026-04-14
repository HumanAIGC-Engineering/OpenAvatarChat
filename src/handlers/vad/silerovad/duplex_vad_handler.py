"""
Duplex VAD Handler - Always-on VAD for Full-Duplex Conversation

This handler extends the standard Silero VAD to support full-duplex mode:
- Always processes audio (ignores CLIENT_PLAYBACK stream lifecycle signals)
- Outputs HUMAN_DUPLEX_AUDIO instead of HUMAN_AUDIO
- Listens for SEMANTIC_WAIT signal to extend waiting time
"""

from typing import cast, Dict

from loguru import logger

from chat_engine.common.handler_base import HandlerDataInfo, HandlerDetail
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry

from handlers.vad.silerovad.vad_handler_silero import (
    HandlerAudioVAD, 
    HumanAudioVADContext,
    SileroVADConfigModel,
    SpeakingStatus
)


class DuplexVADContext(HumanAudioVADContext):
    """Context for Duplex VAD with semantic wait support"""
    
    def __init__(self, session_id: str):
        super().__init__(session_id)
        # Flag set by SEMANTIC_WAIT signal to extend wait time
        self.extend_wait_requested: bool = False
        # Additional silence duration to wait when semantic wait is requested
        self.extended_wait_samples: int = 0
        # Avatar speaking state at stream start - recorded when entering START state
        # This state persists throughout the VAD cycle (START -> POST_END) and is cleared when POST_END ends
        self.avatar_was_speaking_at_stream_start: bool = False


class DuplexVADHandler(HandlerAudioVAD):
    """
    Duplex VAD Handler - Always-on VAD for full-duplex mode.
    
    Key differences from standard VAD:
    1. Outputs HUMAN_DUPLEX_AUDIO instead of HUMAN_AUDIO
    2. Ignores CLIENT_PLAYBACK stream signals (always processes audio)
    3. Listens for SEMANTIC_WAIT to extend waiting time
    """
    
    def create_context(self, session_context: SessionContext, handler_config=None) -> HandlerContext:
        context = DuplexVADContext(session_context.session_info.session_id)
        context.shared_states = session_context.shared_states
        if isinstance(handler_config, SileroVADConfigModel):
            context.config = handler_config
        context.slice_context = self._create_slice_context(context)
        context.history_length_limit = self._calculate_history_limit(context)
        context.agc = self._create_agc()
        context.reset_model()
        return context

    def _create_slice_context(self, context: DuplexVADContext):
        from engine_utils.general_slicer import SliceContext
        return SliceContext.create_numpy_slice_context(
            slice_size=context.clip_size,
            slice_axis=0,
        )
    
    def _calculate_history_limit(self, context: DuplexVADContext) -> int:
        import math
        return math.ceil((context.config.start_delay + context.config.buffer_look_back)
                        / context.clip_size)
    
    def _create_agc(self):
        from engine_utils.audio_utils import create_mel_agc
        return create_mel_agc(
            target_level_db=-5.0,
            max_gain_db=30.0,
            min_gain_db=-30.0,
            attack_time_ms=5.0,
            release_time_ms=50.0,
            sample_rate=16000,
            n_mels=80,
            n_fft=1024,
            hop_length=256,
        )

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_audio_entry("human_duplex_audio", 1, 16000))
        return HandlerDetail(
            inputs=[
                HandlerDataInfo(type=ChatDataType.MIC_AUDIO)
            ],
            outputs=[
                # Output HUMAN_DUPLEX_AUDIO instead of HUMAN_AUDIO
                HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_AUDIO, definition=definition)
            ],
            signal_filters=[
                # Listen for SEMANTIC_WAIT signal to extend waiting time
                SignalFilterRule(ChatSignalType.SEMANTIC_WAIT, None, None),
                # Still listen for candidate STREAM_END for EOU collaboration
                SignalFilterRule(ChatSignalType.STREAM_END, None, ChatDataType.HUMAN_DUPLEX_AUDIO)
            ]
        )

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        context = cast(DuplexVADContext, context)
        output_definition = output_definitions.get(ChatDataType.HUMAN_DUPLEX_AUDIO)
        if output_definition is None:
            logger.warning("HUMAN_DUPLEX_AUDIO output definition not found")
            return
        
        # In duplex mode, always process audio regardless of playback state
        # This is the key difference from standard VAD
        if inputs.type != ChatDataType.MIC_AUDIO:
            return

        # Call parent's processing logic but with modified behavior
        self._handle_audio_input(context, inputs, output_definition.definition)

    def _handle_audio_input(self, context: DuplexVADContext, inputs: ChatData, 
                            output_definition: DataBundleDefinition):
        """Process audio input with duplex-specific logic"""
        import numpy as np
        from engine_utils.general_slicer import slice_data
        from chat_engine.data_models.runtime_data.event_model import EventType
        from chat_engine.data_models.runtime_data.data_bundle import DataBundle
        from chat_engine.data_models.chat_signal_type import ChatSignalSourceType

        audio = inputs.data.get_main_data()
        if audio is None:
            return
        audio_entry = inputs.data.get_main_definition_entry()
        sample_rate = audio_entry.sample_rate
        audio = audio.squeeze()

        if context.agc is not None:
            context.agc.update_gain(audio)

        timestamp = None
        if inputs.is_timestamp_valid():
            timestamp = inputs.timestamp

        if audio.dtype != np.float32:
            audio = audio.astype(np.float32) / 32767

        context.slice_context.update_start_id(timestamp[0], force_update=False)

        for clip in slice_data(context.slice_context, audio):
            from engine_utils.audio_utils import AudioUtils
            rms = AudioUtils.get_rms(clip, self.weight_curve)
            db = AudioUtils.rms_to_db(rms)
            context.current_db = db  # 保存当前能量，用于 POST_END 的备份检测
            if db > context.peak_volume:
                context.peak_volume = db
            head_sample_id = context.slice_context.get_last_slice_start_index()
            speech_prob = self._inference(context, clip)
            if (context.speaking_status in (SpeakingStatus.END, SpeakingStatus.POST_END)
                and db < context.config.volume_threshold):
                speech_prob = 0.0
            
            if context.peak_volume > -100:
                context.peak_volume -= 1.0
            
            # Handle semantic wait extension
            if context.extend_wait_requested and context.speaking_status == SpeakingStatus.START:
                # Extend the silence tolerance when semantic wait is requested
                context.extended_wait_samples += context.clip_size
                if context.extended_wait_samples < context.config.end_delay:
                    # Artificially reduce silence length to delay end detection
                    context.silence_length = max(0, context.silence_length - context.clip_size)
                else:
                    # Reset after extended wait period
                    context.extend_wait_requested = False
                    context.extended_wait_samples = 0
            
            audio_clip, extra_args = context.update_status(speech_prob, clip, timestamp=head_sample_id)
            
            human_speech_start = extra_args.get("human_speech_start", False)
            human_speech_end = extra_args.get("human_speech_end", False)
            back_to_end = extra_args.get("back_to_end", False)
            entering_post_end = extra_args.get("entering_post_end", False)
            reconnect_triggered = extra_args.get("reconnect_triggered", False)
            post_end_timeout = extra_args.get("post_end_timeout", False)
            timestamp_val = extra_args.get("head_sample_id", head_sample_id)
            speech_id = f"duplex-{context.session_id}-{context.speech_id}"
            
            # Check avatar speaking state when entering START state
            if human_speech_start:
                # Check if avatar is speaking at the moment we enter START state
                # Use current time since stream hasn't been created yet
                import time
                check_timestamp = time.monotonic()
                if context.session_history:
                    is_avatar_speaking = context.session_history.was_avatar_speaking_at(check_timestamp)
                    context.avatar_was_speaking_at_stream_start = is_avatar_speaking
                    logger.info(
                        f"Duplex VAD: Entering START state, avatar_was_speaking_at_stream_start={is_avatar_speaking} "
                        f"(checked at timestamp {check_timestamp:.3f})"
                    )
                else:
                    # No session history available, default to False
                    context.avatar_was_speaking_at_stream_start = False
                    logger.warning("Duplex VAD: No session_history available, defaulting avatar_was_speaking_at_stream_start=False")
            
            # Handle POST_END entry
            if entering_post_end:
                streamer = context.data_submitter.get_streamer(ChatDataType.HUMAN_DUPLEX_AUDIO)
                if streamer and streamer.current_stream:
                    context.previous_stream_id = streamer.current_stream.identity
                context.previous_stream_audio = context.current_stream_audio.copy()
                context.current_stream_audio.clear()
                logger.info(f"Duplex VAD entering POST_END, buffered {len(context.previous_stream_audio)} clips")
            
            # Handle reconnection
            if reconnect_triggered:
                self._handle_reconnection_duplex(context, output_definition, sample_rate, speech_id)
            
            if post_end_timeout:
                logger.info("Duplex VAD POST_END timeout, clearing buffers")
                # Clear avatar speaking state - VAD cycle is completely ended
                context.avatar_was_speaking_at_stream_start = False
                logger.debug("Duplex VAD: Cleared avatar_was_speaking_at_stream_start state (POST_END timeout)")
            
            # In duplex mode, we don't disable VAD on speech end
            # This is handled by the semantic turn detector instead
            
            if back_to_end:
                context.reset()
                context.reset_model()
                # Reset semantic wait state
                context.extend_wait_requested = False
                context.extended_wait_samples = 0
                # Clear avatar speaking state - VAD cycle is completely ended
                context.avatar_was_speaking_at_stream_start = False
                logger.debug("Duplex VAD: Cleared avatar_was_speaking_at_stream_start state (back_to_end)")
            
            if audio_clip is not None:
                if context.agc is not None:
                    audio_clip = context.agc.apply_gain(audio_clip)
                
                if context.speaking_status == SpeakingStatus.START or entering_post_end:
                    context.current_stream_audio.append(audio_clip.copy())
                    context.accumulated_speech_audio.append(audio_clip.copy())  # 持久累积
                
                output = DataBundle(output_definition)
                output.set_main_data(np.expand_dims(audio_clip, axis=0))
                for flag_name, flag_value in extra_args.items():
                    output.add_meta(flag_name, flag_value)
                
                if extra_args.get("early_vad_end", False):
                    output.add_event_by_type(EventType.EVT_EARLY_VAD_END)

                output_chat_data = ChatData(
                    type=ChatDataType.HUMAN_DUPLEX_AUDIO,
                    data=output
                )
                if human_speech_end:
                    output_chat_data.is_last_data = True
                if timestamp_val >= 0:
                    output_chat_data.timestamp = timestamp_val, sample_rate
                
                # Check if this is the first data of a new stream (human_speech_start)
                # If so, set inheritable metadata with avatar speaking state
                is_first_data_of_stream = human_speech_start
                
                context.submit_data(output_chat_data, finish_stream=output_chat_data.is_last_data)
                
                streamer = context.data_submitter.get_streamer(ChatDataType.HUMAN_DUPLEX_AUDIO)
                if streamer and streamer.current_stream:
                    context.current_stream_id = streamer.current_stream.identity
                    
                    # Set inheritable metadata when entering START state (first data of stream)
                    if is_first_data_of_stream:
                        streamer.current_stream.update_inheritable_metadata({
                            "avatar_was_speaking_at_stream_start": context.avatar_was_speaking_at_stream_start
                        }, inherit=True)
                        logger.info(
                            f"Duplex VAD: Set inheritable metadata for stream {streamer.current_stream.identity}, "
                            f"avatar_was_speaking_at_stream_start={context.avatar_was_speaking_at_stream_start}"
                        )

    def _handle_reconnection_duplex(self, context: DuplexVADContext, output_definition,
                                    sample_rate: int, speech_id: str):
        """Handle reconnection in duplex mode"""
        import numpy as np
        from chat_engine.data_models.runtime_data.data_bundle import DataBundle

        logger.info(f"Duplex VAD handling reconnection")
        
        if context.previous_stream_id:
            streamer = context.data_submitter.get_streamer(ChatDataType.HUMAN_DUPLEX_AUDIO)
            if streamer:
                cancelled = streamer.cancel_stream(context.previous_stream_id)
                if cancelled:
                    logger.info(f"Cancelled duplex stream: {context.previous_stream_id}")
        
        # Send all accumulated audio to new stream
        # 使用 accumulated_speech_audio 确保所有音频都被发送，即使多次 reconnection
        total_clips = len(context.accumulated_speech_audio)
        
        if context.accumulated_speech_audio:
            logger.info(f"Sending {total_clips} accumulated clips to new duplex stream")
            for clip_index, buffered_clip in enumerate(context.accumulated_speech_audio):
                output = DataBundle(output_definition)
                output.set_main_data(np.expand_dims(buffered_clip, axis=0))
                output.add_meta("reconnected_audio", True)
                output.add_meta("reconnected_audio_index", clip_index)
                
                output_chat_data = ChatData(
                    type=ChatDataType.HUMAN_DUPLEX_AUDIO,
                    data=output
                )
                context.submit_data(output_chat_data, finish_stream=False)
            
            # After first submit_data, the new stream is created. Set inheritable metadata
            # to mark this as a POST_END reconnection stream, so downstream handlers
            # (like SemanticTurnDetector) can treat it as continuous speech input.
            # Use the already recorded avatar speaking state (same VAD cycle).
            streamer = context.data_submitter.get_streamer(ChatDataType.HUMAN_DUPLEX_AUDIO)
            if streamer and streamer.current_stream and context.previous_stream_id:
                # Use stream_key_str to ensure client receives a simple stream_key string
                # that can be directly compared with their own stream_key values
                previous_stream_key = context.previous_stream_id.stream_key_str
                if previous_stream_key:
                    inheritable_metadata = {
                        "continue_from_stream": previous_stream_key,
                        "avatar_was_speaking_at_stream_start": context.avatar_was_speaking_at_stream_start
                    }
                    streamer.current_stream.update_inheritable_metadata(inheritable_metadata, inherit=True)
                    logger.info(
                        f"Marked stream {streamer.current_stream.identity} as POST_END reconnection "
                        f"(continue_from_stream={previous_stream_key}, "
                        f"avatar_was_speaking_at_stream_start={context.avatar_was_speaking_at_stream_start}, "
                        f"inheritable metadata will be passed to downstream streams)"
                    )
                else:
                    logger.warning(
                        f"Cannot set continue_from_stream: previous_stream_id {context.previous_stream_id} "
                        f"has no valid stream_key_str"
                    )
        
        logger.info(f"Total {total_clips} buffered clips sent to new duplex stream")
        
        # 清理临时状态，但保留 accumulated_speech_audio（只在 POST_END 真正结束时清空）
        context.post_end_counter = 0
        context.post_end_speech_counter = 0
        context.last_stream_end_time = None
        context.previous_stream_audio.clear()
        context.previous_stream_id = None
        context.current_stream_audio.clear()
        context.post_end_speech_audio.clear()
        
        context.early_vad_end_count = 0
        context.last_early_vad_end_at = 0
        context.candidate_end_received = False
        context.extend_wait_requested = False
        context.extended_wait_samples = 0

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        """Handle signals - particularly SEMANTIC_WAIT for extended waiting"""
        context = cast(DuplexVADContext, context)
        
        if signal.type == ChatSignalType.SEMANTIC_WAIT:
            # Request to extend waiting time (utterance not complete)
            context.extend_wait_requested = True
            context.extended_wait_samples = 0
            logger.debug(f"Duplex VAD received SEMANTIC_WAIT signal, extending wait time")
        elif signal.type == ChatSignalType.STREAM_END and signal.is_candidate:
            # Candidate end signal from EOU
            if (signal.related_stream and 
                context.current_stream_id and
                signal.related_stream.key == context.current_stream_id.key):
                context.candidate_end_received = True
                logger.info(f"Duplex VAD received candidate STREAM_END from {signal.source_name}")


# Export the handler class
handler_class = DuplexVADHandler
