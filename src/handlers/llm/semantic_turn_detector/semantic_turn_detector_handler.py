"""
Semantic Turn Detector Handler

An LLM-based handler for semantic turn detection in full-duplex conversations.
Supports two operation modes:

1. Duplex Mode (duplex_mode=True):
   - Receives HUMAN_DUPLEX_TEXT from ASR
   - Detects interruption when avatar is speaking
   - Detects utterance completion when user is speaking
   - Emits SEMANTIC_WAIT signal to extend VAD waiting time
   - Emits HUMAN_TEXT when utterance is complete

2. Non-Duplex Mode (duplex_mode=False):
   - Listens for INTERRUPT signals from client
   - Performs semantic validation before triggering interruption
   - Works with standard VAD/ASR pipeline
"""
import os
import time
from concurrent.futures import ThreadPoolExecutor, Future
from typing import cast, Dict, Optional, List, Any

import numpy as np
from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.common.handler_base import HandlerBase, HandlerDataInfo, HandlerDetail, HandlerBaseInfo
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalType, ChatSignalSourceType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.contexts.session_history import HistoryEvent
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from chat_engine.data_models.runtime_data.event_model import EventType


class SemanticTurnDetectorConfig(HandlerBaseConfigModel):
    """Configuration for Semantic Turn Detector"""
    # Feature switches
    enable_interrupt_detection: bool = Field(default=True, description="Enable interrupt detection when avatar is speaking")
    enable_completion_detection: bool = Field(default=True, description="Enable semantic end-of-utterance detection")

    # Mode configuration
    duplex_mode: bool = Field(default=True, description="True: process HUMAN_DUPLEX_TEXT; False: only handle INTERRUPT signals")

    # LLM configuration
    api_url: str = Field(default="", description="OpenAI-compatible API URL")
    api_key: str = Field(default="", description="API key")
    model_name: str = Field(default="KE-SemanticVAD", description="Model name")
    max_context_turns: int = Field(default=3, description="Maximum dialog turns to include in context")
    request_timeout: float = Field(default=3.0, description="LLM request timeout in seconds")

    # Interrupt configuration
    interrupt_on_any_speech: bool = Field(default=False, description="True: any speech triggers interrupt; False: semantic judgment")
    min_text_length_for_interrupt: int = Field(default=2, description="Minimum text length to consider for interrupt")

    # Completion detection configuration
    min_text_length_for_completion: int = Field(default=1, description="Minimum text length for completion check")

    # Interrupt intent judgment configuration
    interrupt_judge_api_url: str = Field(default="", description="LLM API URL for interrupt intent judgment")
    interrupt_judge_api_key: str = Field(default="", description="API key for interrupt intent judgment")
    interrupt_judge_model_name: str = Field(default="Qwen3-8B", description="Model name for interrupt intent judgment")


class SemanticTurnDetectorContext(HandlerContext):
    """Context for Semantic Turn Detector"""

    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: SemanticTurnDetectorConfig = SemanticTurnDetectorConfig()
        self.llm_client: Optional[Any] = None
        self.interrupt_judge_llm_client: Optional[Any] = None  # LLM client for interrupt intent judgment

        # Accumulated text for current utterance
        self.current_utterance_text: str = ""
        self.current_utterance_stream_key: Optional[str] = None
        self.current_utterance_start_time: Optional[float] = None  # monotonic timestamp when user started speaking

        # Audio accumulation for partial ASR
        self.current_audio_buffer: List[np.ndarray] = []  # Audio buffer for current stream
        self.current_audio_stream_key: Optional[str] = None  # Current audio stream key

        # Track the current human_duplex_audio stream key
        # Used to pass to HUMAN_TEXT output so client can correlate preset audio tracking
        self.current_human_duplex_audio_stream_key: Optional[str] = None

        # State tracking
        self.last_interrupt_time: float = 0
        self.interrupt_cooldown: float = 1.0  # Cooldown between interrupts
        
        # Deduplication for partial text - use stream_id + text to avoid race conditions
        self.processed_partial_texts: Dict[str, str] = {}  # stream_id -> last_text
        # Legacy deduplication fields (kept for backward compatibility, may be removed later)
        self.last_partial_text: str = ""  # Last processed partial text
        self.last_partial_avatar_text: str = ""  # Avatar text at last processing (to detect new conversation turns)


class SemanticTurnDetectorHandler(HandlerBase):
    """
    Semantic Turn Detector - LLM-based turn detection for full-duplex conversation.
    """

    # Prompt templates
    INTERRUPT_PROMPT = """你是一个对话打断检测器。用户正在和数字人对话，数字人正在播报回复。

最近的对话历史：
{dialog_history}

数字人正在播报的内容（可能尚未完成）：
{avatar_text}

用户刚才说的话：
{user_text}

请判断用户是否想要打断数字人的播报。

判断标准（按优先级排序）：
1. 【打断】用户明确要求暂停、等待或停止播报：
   - 中文：等一下、等等、停、暂停、慢点、别说了
   - 英文：wait、wait a moment、hold on、stop、pause、one moment、just a second
2. 【打断】用户针对当前播报内容提出回应、提问或否定
3. 【打断】用户开始说新的话题或提出新的问题
4. 【不打断】用户只是发出简单的语气词/填充词，没有实际内容：
   - 中文：嗯、哦、啊、好、好的
   - 英文：uh、um、uh-huh、hmm

注意："wait a moment"、"hold on" 等明确表达等待意图的短语必须判断为"打断"。

只回答"打断"或"不打断"，不要有其他内容。"""

    COMPLETION_PROMPT = """你是一个语音结束检测器。用户正在和数字人对话。

最近的对话历史：
{dialog_history}

用户目前说的话（可能尚未说完）：
{user_text}

请判断用户的话是否已经完整表达了意思，可以交给数字人回复。

判断标准：
- 如果句子结构完整、意思明确，判断为"完成"
- 如果句子明显不完整（如"我想要..."、"你能不能..."但没说完），判断为"未完"
- 如果只是语气词或很短的词无法判断，判断为"未完"

只回答"完成"或"未完"，不要有其他内容。"""

    INTERRUPT_INTENT_PROMPT = """You are an interrupt intent analyzer. A user is having a conversation with a digital avatar, and the user interrupted the avatar while it was speaking.

The avatar's current speech content:
{avatar_text}

What the user said when interrupting:
{interrupt_text}

Please analyze the user's interrupt intent and respond strictly according to the following rules:

Rule 1: If the user only wants to stop the current playback (e.g., "stop", "stop it", "enough", "that's enough", "shut up", "be quiet", "cut it out", "hold on", "wait"), respond with: pure_interrupt

Rule 2: If the user raised a new question, new topic, or new request (e.g., "I want to ask...", "Actually...", "Wait, I think...", "But...", "However...", "What about...", "Can you...", "I need...", "I'd like to..."), respond with: has_new_topic

Rule 3: Respond with ONLY "pure_interrupt" or "has_new_topic" (exactly these words, no other content, no punctuation, no explanation).

Your response:
"""

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="SemanticTurnDetector",
            config_model=SemanticTurnDetectorConfig
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        config = cast(SemanticTurnDetectorConfig, handler_config)
        if not config:
            return
        if not config.api_key:
            config.api_key = os.environ.get("SEMANTIC_LLM_EAS_TOKEN", "")
        if not config.api_key:
            config.api_key = os.environ.get("DASHSCOPE_API_KEY", "")
        if not config.interrupt_judge_api_key:
            config.interrupt_judge_api_key = os.environ.get("INTERRUPT_JUDGE_LLM_EAS_TOKEN", "")
        if not config.interrupt_judge_api_key:
            config.interrupt_judge_api_key = os.environ.get("DASHSCOPE_API_KEY", "")

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        context = SemanticTurnDetectorContext(session_context.session_info.session_id)
        if isinstance(handler_config, SemanticTurnDetectorConfig):
            context.config = handler_config
        return context

    def warmup_context(self, session_context: SessionContext, handler_context: HandlerContext):
        context = cast(SemanticTurnDetectorContext, handler_context)
        self._init_llm_client(context)

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def _init_llm_client(self, context: SemanticTurnDetectorContext):
        """Initialize LLM clients (main and interrupt intent judgment)"""
        # Initialize main LLM client for interrupt detection
        logger.info(
            f"SemanticTurnDetector: Initializing main LLM client, "
            f"api_url={context.config.api_url}, "
            f"api_key={'[SET]' if context.config.api_key else '[EMPTY]'}, "
            f"model={context.config.model_name}"
        )

        if context.config.api_url:
            try:
                from openai import OpenAI
                context.llm_client = OpenAI(
                    api_key=context.config.api_key or "dummy",  # Some APIs don't need key
                    base_url=context.config.api_url,
                    timeout=context.config.request_timeout
                )
                logger.info(
                    f"SemanticTurnDetector: Main LLM client initialized successfully, "
                    f"base_url={context.config.api_url}"
                )
            except ImportError:
                logger.warning("SemanticTurnDetector: openai package not installed, LLM features disabled")
            except Exception as e:
                logger.error(f"SemanticTurnDetector: Failed to initialize main LLM client: {e}")
        else:
            logger.warning("SemanticTurnDetector: Main API URL not configured, LLM features disabled")

        # Initialize interrupt intent judgment LLM client
        interrupt_judge_api_key = context.config.interrupt_judge_api_key
        if not interrupt_judge_api_key:
            interrupt_judge_api_key = os.environ.get("INTERRUPT_JUDGE_LLM_EAS_TOKEN", "")
        if not interrupt_judge_api_key:
            interrupt_judge_api_key = os.environ.get("DASHSCOPE_API_KEY", "")

        logger.info(
            f"SemanticTurnDetector: Initializing interrupt intent judgment LLM client, "
            f"api_url={context.config.interrupt_judge_api_url}, "
            f"api_key={'[SET]' if interrupt_judge_api_key else '[EMPTY]'}, "
            f"model={context.config.interrupt_judge_model_name}"
        )

        if context.config.interrupt_judge_api_url:
            try:
                from openai import OpenAI
                context.interrupt_judge_llm_client = OpenAI(
                    api_key=interrupt_judge_api_key or "dummy",
                    base_url=context.config.interrupt_judge_api_url,
                    timeout=context.config.request_timeout
                )
                logger.info(
                    f"SemanticTurnDetector: Interrupt intent judgment LLM client initialized successfully, "
                    f"base_url={context.config.interrupt_judge_api_url}"
                )
            except ImportError:
                logger.warning("SemanticTurnDetector: openai package not installed, interrupt intent judgment disabled")
            except Exception as e:
                logger.error(f"SemanticTurnDetector: Failed to initialize interrupt intent judgment LLM client: {e}")
        else:
            logger.warning("SemanticTurnDetector: Interrupt intent judgment API URL not configured, feature disabled")

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        ctx = cast(SemanticTurnDetectorContext, context)

        inputs = []
        outputs = []
        signal_filters = []

        if ctx.config.duplex_mode:
            # Duplex mode: receive HUMAN_DUPLEX_TEXT, output HUMAN_TEXT
            inputs.append(HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_TEXT))

            # Receive HUMAN_DUPLEX_AUDIO for early interrupt detection
            audio_definition = DataBundleDefinition()
            audio_definition.add_entry(DataBundleEntry.create_audio_entry("human_duplex_audio", 1, 16000))
            inputs.append(HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_AUDIO, definition=audio_definition))

            # Receive HUMAN_DUPLEX_TEXT_PARTIAL from partial ASR
            partial_text_definition = DataBundleDefinition()
            partial_text_definition.add_entry(DataBundleEntry.create_text_entry("human_duplex_text_partial"))
            inputs.append(HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_TEXT_PARTIAL, definition=partial_text_definition))

            # Output HUMAN_TEXT for downstream LLM
            text_definition = DataBundleDefinition()
            text_definition.add_entry(DataBundleEntry.create_text_entry("human_text"))
            outputs.append(HandlerDataInfo(type=ChatDataType.HUMAN_TEXT, definition=text_definition))

            # Output HUMAN_DUPLEX_AUDIO_PARTIAL for partial ASR handler
            partial_audio_definition = DataBundleDefinition()
            partial_audio_definition.add_entry(DataBundleEntry.create_audio_entry("human_duplex_audio_partial", 1, 16000))
            outputs.append(HandlerDataInfo(type=ChatDataType.HUMAN_DUPLEX_AUDIO_PARTIAL, definition=partial_audio_definition))

        # CLIENT INTERRUPT is handled by InterruptHandler (stream cancellation decoupled)

        # Listen for AVATAR_AUDIO stream events to track speaking state
        signal_filters.append(SignalFilterRule(ChatSignalType.STREAM_BEGIN, None, ChatDataType.AVATAR_AUDIO))
        signal_filters.append(SignalFilterRule(ChatSignalType.STREAM_END, None, ChatDataType.AVATAR_AUDIO))

        # Listen for CLIENT_PLAYBACK stream lifecycle to track actual playback state
        signal_filters.append(SignalFilterRule(ChatSignalType.STREAM_BEGIN, None, ChatDataType.CLIENT_PLAYBACK))
        signal_filters.append(SignalFilterRule(ChatSignalType.STREAM_END, None, ChatDataType.CLIENT_PLAYBACK))
        signal_filters.append(SignalFilterRule(ChatSignalType.STREAM_CANCEL, None, ChatDataType.CLIENT_PLAYBACK))

        return HandlerDetail(
            inputs=inputs,
            outputs=outputs,
            signal_filters=signal_filters
        )

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        ctx = cast(SemanticTurnDetectorContext, context)

        if inputs.type == ChatDataType.HUMAN_DUPLEX_TEXT:
            self._handle_duplex_text(ctx, inputs, output_definitions)
        elif inputs.type == ChatDataType.HUMAN_DUPLEX_AUDIO:
            self._handle_duplex_audio(ctx, inputs, output_definitions)
        elif inputs.type == ChatDataType.HUMAN_DUPLEX_TEXT_PARTIAL:
            self._handle_partial_text(ctx, inputs, output_definitions)

    def _handle_duplex_audio(self, context: SemanticTurnDetectorContext, inputs: ChatData,
                            output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """Handle HUMAN_DUPLEX_AUDIO input - accumulate audio and trigger partial ASR on early_vad_end"""
        if inputs.data is None:
            return

        audio = inputs.data.get_main_data()
        if audio is None:
            return

        # Get audio entry info
        audio_entry = inputs.data.get_main_definition_entry()
        if audio_entry is None:
            return

        sample_rate = audio_entry.sample_rate
        audio = audio.squeeze()  # Remove batch dimension if present

        # Check for new stream
        stream_key = inputs.stream_id.key if inputs.stream_id else None
        stream_key_str = inputs.stream_id.stream_key_str if inputs.stream_id else None
        if stream_key != context.current_audio_stream_key:
            # New stream, reset buffer
            context.current_audio_buffer = []
            context.current_audio_stream_key = stream_key
            # Track the human_duplex_audio stream key string for passing to HUMAN_TEXT output
            # Use stream_key_str (string) instead of stream_key (StreamKey object)
            context.current_human_duplex_audio_stream_key = stream_key_str
            logger.debug(f"SemanticTurnDetector: New audio stream detected: {stream_key_str}")

        # Accumulate audio data
        context.current_audio_buffer.append(audio.copy())

        # Check for early_vad_end event
        has_early_end = inputs.data.has_event(EventType.EVT_EARLY_VAD_END) if inputs.data else False

        if has_early_end:
            # Check if avatar is currently speaking
            is_avatar_speaking = False
            if context.session_history:
                current_time = time.monotonic()
                is_avatar_speaking = context.session_history.was_avatar_speaking_at(current_time)

            if is_avatar_speaking and context.config.enable_interrupt_detection:
                # Avatar is speaking and we detected early_vad_end - trigger partial ASR
                if len(context.current_audio_buffer) > 0:
                    # Concatenate all audio chunks
                    concatenated_audio = np.concatenate(context.current_audio_buffer, axis=0)

                    # Send to partial ASR handler
                    if ChatDataType.HUMAN_DUPLEX_AUDIO_PARTIAL in output_definitions:
                        output_def = output_definitions[ChatDataType.HUMAN_DUPLEX_AUDIO_PARTIAL]
                        if output_def.definition is None:
                            definition = DataBundleDefinition()
                            definition.add_entry(DataBundleEntry.create_audio_entry("human_duplex_audio_partial", 1, sample_rate))
                        else:
                            definition = output_def.definition

                        output_bundle = DataBundle(definition)
                        # Audio should be in shape [1, N] for DataBundle
                        output_bundle.set_main_data(np.expand_dims(concatenated_audio, axis=0))

                        # Create new stream for partial audio
                        output_streamer = context.data_submitter.get_streamer(ChatDataType.HUMAN_DUPLEX_AUDIO_PARTIAL)
                        if output_streamer is not None:
                            # Use current input stream as source
                            source_streams = [inputs.stream_id] if inputs.stream_id else []
                            output_streamer.new_stream(source_streams)

                            if output_streamer.current_stream is not None:
                                output_chat_data = ChatData(
                                    type=ChatDataType.HUMAN_DUPLEX_AUDIO_PARTIAL,
                                    data=output_bundle,
                                    is_last_data=True  # Finish stream to trigger ASR
                                )
                                if inputs.timestamp:
                                    output_chat_data.timestamp = inputs.timestamp

                                output_streamer.stream_data(output_bundle, finish_stream=True)
                                logger.info(
                                    f"SemanticTurnDetector: Sent partial audio to ASR handler, "
                                    f"length={len(concatenated_audio)} samples, "
                                    f"stream_key={stream_key}"
                                )
                            else:
                                logger.warning("SemanticTurnDetector: Output stream was auto-cancelled, skipping partial audio")
                        else:
                            logger.warning("SemanticTurnDetector: No HUMAN_DUPLEX_AUDIO_PARTIAL streamer available")
                    else:
                        logger.warning("SemanticTurnDetector: HUMAN_DUPLEX_AUDIO_PARTIAL output not defined")
                else:
                    logger.debug("SemanticTurnDetector: Early VAD end detected but audio buffer is empty")
            else:
                logger.debug(f"SemanticTurnDetector: Early VAD end detected but avatar not speaking (is_avatar_speaking={is_avatar_speaking})")

    def _handle_partial_text(self, context: SemanticTurnDetectorContext, inputs: ChatData,
                            output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """Handle HUMAN_DUPLEX_TEXT_PARTIAL input - perform interrupt detection and intent judgment"""
        text = inputs.data.get_main_data() if inputs.data else None
        if not text:
            return

        logger.info(f"SemanticTurnDetector: Received partial ASR text: {text[:50]}...")

        # Check avatar speaking state from VAD metadata
        # VAD records avatar_was_speaking_at_stream_start when entering START state
        avatar_was_speaking_at_stream_start = False
        if inputs.data and inputs.data.metadata:
            avatar_was_speaking_at_stream_start = inputs.data.metadata.get("avatar_was_speaking_at_stream_start", False)
            logger.info(
                f"SemanticTurnDetector: Partial text metadata - "
                f"avatar_was_speaking_at_stream_start={avatar_was_speaking_at_stream_start}"
            )

        # Only proceed with interrupt detection if avatar was speaking at stream start
        # Skip interrupt detection if avatar was NOT speaking (even if continue_from_stream exists)
        if not avatar_was_speaking_at_stream_start:
            logger.debug(
                f"SemanticTurnDetector: Partial text received but avatar was NOT speaking at stream start, "
                f"skipping interrupt detection"
            )
            return

        # Get stream_id for deduplication
        stream_key = inputs.stream_id.key if inputs.stream_id else None

        # Deduplication: use stream_id + text to avoid race conditions
        # Update state immediately to prevent concurrent requests from both passing the check
        if stream_key:
            last_text = context.processed_partial_texts.get(stream_key)
            if last_text == text:
                logger.debug(
                    f"SemanticTurnDetector: Skipping duplicate partial text for stream {stream_key}: {text[:50]}..."
                )
                return
            # Immediately update state to prevent race condition
            context.processed_partial_texts[stream_key] = text

        # Get current avatar text to check for context change
        current_avatar_text = self._get_current_avatar_text(context)
        
        # Legacy deduplication check (kept for backward compatibility)
        # If avatar_text changed, it's a new conversation turn - should re-process even if user text is same
        is_same_context = (current_avatar_text == context.last_partial_avatar_text)
        is_same_text = (text == context.last_partial_text)
        
        if is_same_text and is_same_context:
            logger.debug(f"SemanticTurnDetector: Skipping duplicate partial text (same text and context): {text[:50]}...")
            return
        
        # Update last partial text and context (legacy fields)
        context.last_partial_text = text
        context.last_partial_avatar_text = current_avatar_text

        # Avatar was speaking at stream start - check for interrupt
        if context.config.enable_interrupt_detection:
            logger.info(
                f"SemanticTurnDetector: Partial text - avatar was speaking at stream start, checking interrupt"
            )
            self._check_interrupt(context, text, inputs, output_definitions)
        else:
            logger.debug(f"SemanticTurnDetector: Partial text received but interrupt detection disabled")

    def _handle_duplex_text(self, context: SemanticTurnDetectorContext, inputs: ChatData,
                           output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """Handle HUMAN_DUPLEX_TEXT input"""
        text = inputs.data.get_main_data()
        if not text:
            return

        # Accumulate text for current utterance
        stream_key = inputs.stream_id.key if inputs.stream_id else None
        if stream_key != context.current_utterance_stream_key:
            # New stream, reset accumulated text
            context.current_utterance_text = text
            context.current_utterance_stream_key = stream_key

            # Get the REAL time when user started speaking from SessionHistory
            # This is the HUMAN_DUPLEX_AUDIO STREAM_BEGIN time, not when ASR result arrives
            if context.session_history:
                context.current_utterance_start_time = context.session_history.get_stream_start_time(
                    ChatDataType.HUMAN_DUPLEX_AUDIO,
                    most_recent=True
                )
                logger.debug(f"SemanticTurnDetector: User speech start time from history: {context.current_utterance_start_time}")

            # Fallback to current time if history lookup failed
            if context.current_utterance_start_time is None:
                context.current_utterance_start_time = time.monotonic()
                logger.warning("SemanticTurnDetector: Could not find HUMAN_DUPLEX_AUDIO start time in history, using current time")
            
            # Check avatar speaking state from VAD metadata
            # VAD records avatar_was_speaking_at_stream_start when entering START state
            # This state persists throughout the VAD cycle and is passed via inheritable metadata
            avatar_was_speaking_at_stream_start = False
            continue_from_stream = None
            if inputs.data and inputs.data.metadata:
                avatar_was_speaking_at_stream_start = inputs.data.metadata.get("avatar_was_speaking_at_stream_start", False)
                continue_from_stream = inputs.data.metadata.get("continue_from_stream")
                
                logger.info(
                    f"SemanticTurnDetector: Stream metadata - "
                    f"avatar_was_speaking_at_stream_start={avatar_was_speaking_at_stream_start}, "
                    f"continue_from_stream={continue_from_stream}"
                )
        else:
            # Same stream, accumulate text
            context.current_utterance_text = text  # ASR usually sends full text
            # Get metadata from current input (should be same as first data)
            avatar_was_speaking_at_stream_start = False
            continue_from_stream = None
            if inputs.data and inputs.data.metadata:
                avatar_was_speaking_at_stream_start = inputs.data.metadata.get("avatar_was_speaking_at_stream_start", False)
                continue_from_stream = inputs.data.metadata.get("continue_from_stream")

        # Decision logic based on avatar_was_speaking_at_stream_start metadata from VAD
        # This is more accurate than checking session_history because VAD records the state
        # at the exact moment of entering START state
        if avatar_was_speaking_at_stream_start and context.config.enable_interrupt_detection:
            # Avatar was speaking when stream started - check for interrupt
            # However, if continue_from_stream exists (POST_END reconnection), we need to check
            # if avatar is actually still speaking, as it may have finished playback
            if continue_from_stream:
                # POST_END reconnection - check if avatar is actually still speaking
                is_avatar_still_speaking = False
                if context.session_history:
                    active_streams = context.session_history.get_active_avatar_streams()
                    is_avatar_still_speaking = len(active_streams) > 0
                
                if is_avatar_still_speaking:
                    # Avatar is still speaking - check for interrupt
                    logger.info(
                        f"SemanticTurnDetector: POST_END reconnection, avatar still speaking, checking interrupt "
                        f"(continue_from_stream={continue_from_stream})"
                    )
                    self._check_interrupt(context, context.current_utterance_text, inputs, output_definitions)
                else:
                    # Avatar has finished playback - treat as passthrough (not an interrupt)
                    logger.info(
                        f"SemanticTurnDetector: POST_END reconnection, avatar finished playback, "
                        f"treating as continuous speech input (passthrough, continue_from_stream={continue_from_stream})"
                    )
                    if inputs.is_last_data:
                        logger.info(
                            f"SemanticTurnDetector: Passing through text (POST_END reconnection after avatar finished): "
                            f"{context.current_utterance_text[:50]}..."
                        )
                        self._submit_human_text(context, context.current_utterance_text, inputs, output_definitions)
            else:
                # Normal interrupt detection (not POST_END reconnection)
                logger.info(
                    f"SemanticTurnDetector: Avatar was speaking at stream start, checking interrupt"
                )
                self._check_interrupt(context, context.current_utterance_text, inputs, output_definitions)
        elif not avatar_was_speaking_at_stream_start:
            # Avatar was NOT speaking when stream started
            # If continue_from_stream exists, this is a POST_END reconnection - passthrough
            # Otherwise, normal processing (completion detection)
            if continue_from_stream:
                # POST_END reconnection - passthrough (treat as continuous speech)
                # Submit text when stream ends (is_last_data=True)
                logger.info(
                    f"SemanticTurnDetector: Avatar was NOT speaking at stream start + continue_from_stream, "
                    f"treating as continuous speech input (passthrough)"
                )
                if inputs.is_last_data:
                    logger.info(
                        f"SemanticTurnDetector: Passing through text (POST_END reconnection, completion detection disabled): "
                        f"{context.current_utterance_text[:50]}..."
                    )
                    self._submit_human_text(context, context.current_utterance_text, inputs, output_definitions)
            elif context.config.enable_completion_detection:
                # Normal processing - handle based on completion detection setting
                if inputs.is_last_data:
                    # Stream ended, submit the text
                    self._submit_human_text(context, context.current_utterance_text, inputs, output_definitions)
                else:
                    # Check if utterance is complete
                    self._check_completion(context, context.current_utterance_text, inputs, output_definitions)
            else:
                # Completion detection disabled - submit text when stream ends
                if inputs.is_last_data:
                    logger.info(f"SemanticTurnDetector: Passing through text (completion detection disabled): {context.current_utterance_text[:50]}...")
                    self._submit_human_text(context, context.current_utterance_text, inputs, output_definitions)

    def _check_interrupt(self, context: SemanticTurnDetectorContext, text: str, inputs: ChatData,
                        output_definitions: Optional[Dict[ChatDataType, HandlerDataInfo]] = None):
        """Check if user wants to interrupt avatar"""
        if len(text) < context.config.min_text_length_for_interrupt:
            return

        # Cooldown check
        now = time.monotonic()
        if now - context.last_interrupt_time < context.interrupt_cooldown:
            return

        # Fast path: Check if it's a pure stop command using heuristic
        # This is more reliable than LLM for obvious stop commands like "stop", "wait a moment", etc.
        if self._is_pure_stop_command(text):
            logger.info(f"SemanticTurnDetector: Detected pure stop command via heuristic, triggering interrupt: {text[:50]}...")
            self._emit_interrupt_and_cancel(context, text, inputs, output_definitions, should_send_text=False)
            return

        # Get avatar text once to avoid repeated queries
        avatar_text = self._get_current_avatar_text(context)

        if context.config.interrupt_on_any_speech:
            # Any speech triggers interrupt - judge intent
            intent = self._judge_interrupt_intent(context, text, avatar_text)
            should_send_text = (intent == "has_new_topic")
            self._emit_interrupt_and_cancel(context, text, inputs, output_definitions, should_send_text)
            return

        # Semantic judgment
        if context.llm_client is None:
            # No LLM, fall back to any-speech mode - judge intent
            intent = self._judge_interrupt_intent(context, text, avatar_text)
            should_send_text = (intent == "has_new_topic")
            self._emit_interrupt_and_cancel(context, text, inputs, output_definitions, should_send_text)
            return

        # Parallel execution of two LLM calls for better performance
        # First call: detect if user wants to interrupt
        # Second call: judge interrupt intent (pure_interrupt vs has_new_topic)
        executor = ThreadPoolExecutor(max_workers=2)
        future_interrupt = None
        future_intent = None

        try:
            # Start both LLM calls in parallel
            future_interrupt = executor.submit(self._detect_interrupt_llm, context, text, avatar_text)
            future_intent = executor.submit(self._judge_interrupt_intent, context, text, avatar_text)

            # Wait for first call (interrupt detection) to complete
            result_interrupt = future_interrupt.result()

            if result_interrupt == "打断":
                # Interrupt detected - send signal immediately without waiting for intent judgment
                # Send interrupt signal first (without HUMAN_TEXT)
                self._emit_interrupt_and_cancel(context, text, inputs, output_definitions, should_send_text=False)

                # Then wait for intent judgment to complete (can be delayed)
                # This determines whether to send HUMAN_TEXT to downstream LLM
                intent = "has_new_topic"  # Default value
                try:
                    # Wait for intent judgment to complete (may take time, but interrupt signal already sent)
                    intent = future_intent.result()
                    logger.info(f"SemanticTurnDetector: Intent judgment completed: {intent}")
                except Exception as e:
                    logger.warning(f"SemanticTurnDetector: Error getting intent result: {e}, using default")
                    intent = "has_new_topic"

                # If intent is has_new_topic, send HUMAN_TEXT to downstream LLM
                if intent == "has_new_topic" and output_definitions and ChatDataType.HUMAN_TEXT in output_definitions:
                    if inputs is not None:
                        logger.info(f"SemanticTurnDetector: Interrupt has new topic, sending trigger text as HUMAN_TEXT: {text[:50]}...")
                        self._submit_human_text(context, text, inputs, output_definitions)
                    else:
                        logger.warning("SemanticTurnDetector: Cannot send HUMAN_TEXT - inputs is None")
            else:
                # No interrupt detected - cancel intent judgment call if possible
                # Note: OpenAI client may not support cancellation, but we try anyway
                if future_intent and not future_intent.done():
                    cancelled = future_intent.cancel()
                    if cancelled:
                        logger.debug("SemanticTurnDetector: Cancelled intent judgment call (no interrupt detected)")
                    else:
                        logger.debug("SemanticTurnDetector: Could not cancel intent judgment call (may already be running)")
                logger.debug(f"SemanticTurnDetector: No interrupt, user said: {text[:50]}...")
        except Exception as e:
            logger.error(f"SemanticTurnDetector: Error in parallel LLM calls: {e}")
            # Fallback to sequential execution on error
            try:
                result = self._detect_interrupt_llm(context, text, avatar_text)
                if result == "打断":
                    intent = self._judge_interrupt_intent(context, text, avatar_text)
                    should_send_text = (intent == "has_new_topic")
                    self._emit_interrupt_and_cancel(context, text, inputs, output_definitions, should_send_text)
            except Exception as fallback_error:
                logger.error(f"SemanticTurnDetector: Fallback execution also failed: {fallback_error}")
        finally:
            # Shutdown executor without waiting (let background tasks complete)
            executor.shutdown(wait=False)

    def _detect_interrupt_llm(self, context: SemanticTurnDetectorContext, user_text: str, avatar_text: str) -> str:
        """Use LLM to detect if user wants to interrupt

        Args:
            context: Handler context
            user_text: User's speech text
            avatar_text: Current avatar speech text (pre-fetched to avoid repeated queries)
        """
        try:
            # Get dialog history
            dialog_history = self._get_dialog_history(context)

            prompt = self.INTERRUPT_PROMPT.format(
                dialog_history=dialog_history,
                avatar_text=avatar_text,
                user_text=user_text
            )

            # Log request details
            logger.info(
                f"SemanticTurnDetector LLM request: "
                f"api_url={context.config.api_url}, "
                f"model={context.config.model_name}, "
                f"user_text={user_text[:50]}..."
            )
            logger.info(f"SemanticTurnDetector LLM prompt: {prompt}")

            response = context.llm_client.chat.completions.create(
                model=context.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            # Log response details
            result = response.choices[0].message.content.strip()
            logger.info(f"SemanticTurnDetector LLM response: result={result}, model={response.model}")
            return result
        except Exception as e:
            # Log detailed error info
            logger.error(
                f"SemanticTurnDetector: LLM interrupt detection failed: {e}, "
                f"api_url={context.config.api_url}, "
                f"model={context.config.model_name}"
            )
            return "打断"  # Default to interrupt on error

    def _check_completion(self, context: SemanticTurnDetectorContext, text: str,
                          inputs: ChatData, output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """Check if user utterance is complete"""
        if len(text) < context.config.min_text_length_for_completion:
            # Too short, request extended wait
            self._emit_semantic_wait(context)
            return

        if context.llm_client is None:
            # No LLM, can't detect completion
            return

        result = self._detect_completion_llm(context, text)
        if result == "未完":
            self._emit_semantic_wait(context)
        else:
            # Completion detected, submit text
            self._submit_human_text(context, text, inputs, output_definitions)

    def _detect_completion_llm(self, context: SemanticTurnDetectorContext, user_text: str) -> str:
        """Use LLM to detect if utterance is complete"""
        try:
            dialog_history = self._get_dialog_history(context)

            prompt = self.COMPLETION_PROMPT.format(
                dialog_history=dialog_history,
                user_text=user_text
            )

            response = context.llm_client.chat.completions.create(
                model=context.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )

            result = response.choices[0].message.content.strip()
            logger.debug(f"SemanticTurnDetector completion detection: {result}")
            return result
        except Exception as e:
            logger.error(f"SemanticTurnDetector: LLM completion detection failed: {e}")
            return "完成"  # Default to complete on error

    def _get_dialog_history(self, context: SemanticTurnDetectorContext) -> str:
        """Get recent dialog history as formatted string"""
        if context.session_history is None:
            return "(无历史记录)"

        events = context.session_history.get_recent_dialog(
            max_turns=context.config.max_context_turns
        )

        if not events:
            return "(无历史记录)"

        lines = []
        for event in events:
            # Skip events with no meaningful data
            data_text = event.data if event.data else "(未获取到内容)"
            if event.data_type == ChatDataType.HUMAN_TEXT:
                lines.append(f"用户: {data_text}")
            elif event.data_type == ChatDataType.HUMAN_DUPLEX_TEXT:
                lines.append(f"用户: {data_text}")
            elif event.data_type == ChatDataType.AVATAR_TEXT:
                lines.append(f"数字人: {data_text}")

        return "\n".join(lines) if lines else "(无历史记录)"

    def _get_current_avatar_text(self, context: SemanticTurnDetectorContext) -> str:
        """Get the current avatar speech text (may be incomplete)"""
        if context.session_history is None:
            return "(无内容)"

        # Find the most recent AVATAR_TEXT events from the current stream
        events = context.session_history.get_recent_events(
            data_types=[ChatDataType.AVATAR_TEXT],
            max_count=20  # Get more events to aggregate full text
        )

        if not events:
            return "(无内容)"

        # Group by stream and get the most recent stream's aggregated text
        # AVATAR_TEXT is streamed, so we need to aggregate all chunks
        stream_texts: Dict[str, List[str]] = {}
        stream_order: List[str] = []

        for e in events:
            key = e.source_stream_key or e.event_id
            if key not in stream_texts:
                stream_texts[key] = []
                stream_order.append(key)
            if e.data:
                text = str(e.data).strip()
                if text:
                    stream_texts[key].append(text)

        # Get the most recent stream's text
        if stream_order:
            recent_key = stream_order[-1]
            texts = stream_texts[recent_key]
            if texts:
                return "".join(texts)

        return "(无内容)"

    def _is_pure_stop_command(self, text: str) -> bool:
        """Check if the text is a pure stop/pause command without new topic

        This is used as a heuristic fallback when LLM intent judgment fails.
        """
        text_lower = text.lower().strip()
        # Remove common punctuation
        text_clean = text_lower.rstrip('.,!?。，！？')

        # Pure stop commands in English
        stop_commands_en = {
            'stop', 'stop it', 'stop now', 'stop please', 'stop play', 'stop playing',
            'pause', 'pause it', 'pause please',
            'enough', 'that\'s enough', 'thats enough',
            'shut up', 'be quiet', 'quiet',
            'hold on', 'wait', 'wait a moment', 'wait a second', 'one moment',
            'okay stop', 'ok stop', 'please stop',
        }

        # Pure stop commands in Chinese
        stop_commands_zh = {
            '停', '停止', '停下', '停下来', '停一下', '停一停',
            '暂停', '暂停一下',
            '等等', '等一下', '等一等', '等会',
            '别说了', '不要说了', '别讲了', '不要讲了',
            '够了', '可以了', '好了', '行了',
            '安静', '闭嘴',
        }

        # Check exact match
        if text_clean in stop_commands_en or text_clean in stop_commands_zh:
            return True

        # Check if text starts with stop command and is short (less than 30 chars)
        if len(text_clean) < 30:
            for cmd in stop_commands_en | stop_commands_zh:
                if text_clean.startswith(cmd) or text_clean.endswith(cmd):
                    return True

        return False

    def _judge_interrupt_intent(self, context: SemanticTurnDetectorContext, interrupt_text: str, avatar_text: str) -> str:
        """Use LLM to judge interrupt intent: pure_interrupt or has_new_topic

        Args:
            context: Handler context
            interrupt_text: Text that triggered the interrupt
            avatar_text: Current avatar speech text (pre-fetched to avoid repeated queries)
        """
        # First check if it's a pure stop command using heuristic
        # This is a fast path that doesn't require LLM
        if self._is_pure_stop_command(interrupt_text):
            logger.info(f"SemanticTurnDetector: Detected pure stop command via heuristic: {interrupt_text[:50]}...")
            return "pure_interrupt"

        if context.interrupt_judge_llm_client is None:
            logger.warning("SemanticTurnDetector: Interrupt intent judgment LLM client not available, defaulting to has_new_topic")
            return "has_new_topic"  # Default to has_new_topic to be safe

        try:
            prompt = self.INTERRUPT_INTENT_PROMPT.format(
                avatar_text=avatar_text,
                interrupt_text=interrupt_text
            )

            logger.info(
                f"SemanticTurnDetector: Interrupt intent judgment request, "
                f"api_url={context.config.interrupt_judge_api_url}, "
                f"model={context.config.interrupt_judge_model_name}, "
                f"interrupt_text={interrupt_text[:50]}..."
            )

            response = context.interrupt_judge_llm_client.chat.completions.create(
                model=context.config.interrupt_judge_model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=15,
                temperature=0.1,
                # Disable thinking for Qwen3 - use chat_template_kwargs for vLLM/PAI-EAS
                extra_body={"chat_template_kwargs": {"enable_thinking": False}}
            )

            result = response.choices[0].message.content.strip()
            logger.info(f"SemanticTurnDetector: Interrupt intent judgment response: {result}")

            # Remove <think>...</think> tags if present (some models may still include them)
            import re
            result_cleaned = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL).strip()
            # Also handle incomplete thinking tags (response may be truncated)
            result_cleaned = re.sub(r'<think>.*$', '', result_cleaned, flags=re.DOTALL).strip()

            if result_cleaned != result:
                logger.info(f"SemanticTurnDetector: Cleaned thinking tags from response: {result_cleaned}")
                result = result_cleaned

            # Validate and normalize result
            result_lower = result.lower()
            if "pure_interrupt" in result_lower:
                return "pure_interrupt"
            elif "has_new_topic" in result_lower or "new_topic" in result_lower:
                return "has_new_topic"
            else:
                # LLM response was unexpected - use heuristic fallback
                logger.warning(f"SemanticTurnDetector: Unexpected interrupt intent judgment result: {result}")
                # For safety, if we can't determine intent and text is short, assume pure_interrupt
                if len(interrupt_text.strip()) < 50:
                    logger.info(f"SemanticTurnDetector: Short text with unclear intent, defaulting to pure_interrupt")
                    return "pure_interrupt"
                else:
                    logger.info(f"SemanticTurnDetector: Longer text with unclear intent, defaulting to has_new_topic")
                    return "has_new_topic"

        except Exception as e:
            logger.error(
                f"SemanticTurnDetector: Interrupt intent judgment failed: {e}, "
                f"api_url={context.config.interrupt_judge_api_url}, "
                f"model={context.config.interrupt_judge_model_name}"
            )
            # On error, use heuristic: short text is likely pure interrupt
            if len(interrupt_text.strip()) < 50:
                return "pure_interrupt"
            return "has_new_topic"

    def _emit_interrupt_and_cancel(self, context: SemanticTurnDetectorContext, trigger_text: str,
                                   inputs: Optional[ChatData] = None,
                                   output_definitions: Optional[Dict[ChatDataType, HandlerDataInfo]] = None,
                                   should_send_text: bool = False):
        """Emit INTERRUPT signal. Stream cancellation is handled by InterruptHandler.

        Handler responsibility: decide WHEN to interrupt (algorithm) and emit the signal.
        InterruptHandler responsibility: cancel stream chains (HOW).

        Args:
            context: Handler context
            trigger_text: Text that triggered the interrupt
            inputs: Original ChatData input (for stream_id reference), optional
            output_definitions: Output definitions for sending HUMAN_TEXT if needed
            should_send_text: Whether to send trigger_text as HUMAN_TEXT to downstream LLM
        """
        logger.info(f"SemanticTurnDetector: Triggering interrupt, user said: {trigger_text[:50]}..., should_send_text={should_send_text}")

        context.last_interrupt_time = time.monotonic()

        # Check if there are active playback streams to interrupt
        has_active_playback = False
        if context.stream_manager:
            active_playback = [
                s for s in context.stream_manager.get_active_streams()
                if s.identity.data_type == ChatDataType.CLIENT_PLAYBACK
            ]
            has_active_playback = len(active_playback) > 0
        elif context.session_history is not None:
            active_playback_events = context.session_history.get_active_avatar_streams()
            has_active_playback = bool(active_playback_events)

        if not has_active_playback:
            logger.debug("SemanticTurnDetector: No active playback streams to interrupt")
            if should_send_text and output_definitions and ChatDataType.HUMAN_TEXT in output_definitions:
                if inputs is not None:
                    logger.info(f"SemanticTurnDetector: Avatar finished, sending text without interrupt: {trigger_text[:50]}...")
                    self._submit_human_text(context, trigger_text, inputs, output_definitions)
            return

        # Emit INTERRUPT signal — InterruptHandler will handle stream cancellation and history
        interrupt_signal = ChatSignal(
            type=ChatSignalType.INTERRUPT,
            source_type=ChatSignalSourceType.HANDLER,
            source_name=context.owner,
            signal_data={
                "reason": "semantic_interrupt",
                "trigger_text": trigger_text[:100],
            }
        )
        context.emit_signal(interrupt_signal)

        # If interrupt carries new topic, send trigger_text as HUMAN_TEXT to downstream LLM
        if should_send_text and output_definitions and ChatDataType.HUMAN_TEXT in output_definitions:
            if inputs is None:
                logger.warning("SemanticTurnDetector: should_send_text=True but inputs is None")
            else:
                logger.info(f"SemanticTurnDetector: Sending trigger text as HUMAN_TEXT: {trigger_text[:50]}...")
                self._submit_human_text(context, trigger_text, inputs, output_definitions)

    def _emit_semantic_wait(self, context: SemanticTurnDetectorContext):
        """Emit SEMANTIC_WAIT signal to extend VAD waiting time"""
        wait_signal = ChatSignal(
            type=ChatSignalType.SEMANTIC_WAIT,
            source_type=ChatSignalSourceType.HANDLER,
            source_name=context.owner,
        )
        context.emit_signal(wait_signal)
        logger.debug("SemanticTurnDetector: Emitted SEMANTIC_WAIT signal")

    def _submit_human_text(self, context: SemanticTurnDetectorContext, text: str,
                          inputs: ChatData, output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """Submit HUMAN_TEXT to downstream LLM"""
        if ChatDataType.HUMAN_TEXT not in output_definitions:
            return

        output_def = output_definitions[ChatDataType.HUMAN_TEXT]
        if output_def.definition is None:
            definition = DataBundleDefinition()
            definition.add_entry(DataBundleEntry.create_text_entry("human_text"))
        else:
            definition = output_def.definition

        output_bundle = DataBundle(definition)
        output_bundle.set_main_data(text)
        output_bundle.metadata.update(inputs.data.metadata)

        # Add the human_duplex_audio stream key to metadata
        # This allows client to correctly track preset audio playback using continue_from_stream
        if context.current_human_duplex_audio_stream_key:
            output_bundle.add_meta("human_duplex_audio_stream_key", context.current_human_duplex_audio_stream_key)
            logger.debug(
                f"SemanticTurnDetector: Added human_duplex_audio_stream_key={context.current_human_duplex_audio_stream_key} "
                f"to HUMAN_TEXT metadata"
            )

        # 明确指定只使用当前 input stream 作为唯一的 source
        # 这确保 HUMAN_TEXT 只关联到一个 HUMAN_DUPLEX_TEXT，而不是多个
        output_streamer = context.data_submitter.get_streamer(ChatDataType.HUMAN_TEXT)
        if output_streamer is None:
            logger.warning("SemanticTurnDetector: No HUMAN_TEXT streamer available")
            return

        # 使用 inputs.stream_id 作为唯一的 source stream
        source_streams = [inputs.stream_id] if inputs.stream_id else []
        output_streamer.new_stream(source_streams)

        # 检查 stream 是否被 auto-cancel（因为 parent 被 cancel）
        # 如果是，跳过 stream_data，避免触发自动收集所有 input streams 的机制
        if output_streamer.current_stream is None:
            logger.info(f"SemanticTurnDetector: Output stream was auto-cancelled, skipping output")
            return

        output_streamer.stream_data(output_bundle, finish_stream=True)
        logger.info(f"SemanticTurnDetector: Submitted HUMAN_TEXT: {text[:50]}...")

        # Reset accumulated text
        context.current_utterance_text = ""
        context.current_utterance_stream_key = None

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        """Handle signals — CLIENT INTERRUPT is handled by InterruptHandler"""
        ctx = cast(SemanticTurnDetectorContext, context)

        if (signal.related_stream is not None
              and signal.related_stream.data_type == ChatDataType.CLIENT_PLAYBACK):
            stream_key = signal.related_stream.stream_key_str
            logger.info(f"Received CLIENT_PLAYBACK {signal.type.value} for stream_key={stream_key}")

    def destroy_context(self, context: HandlerContext):
        ctx = cast(SemanticTurnDetectorContext, context)
        ctx.llm_client = None
        ctx.interrupt_judge_llm_client = None
        # Clear audio buffer
        ctx.current_audio_buffer = []
        ctx.current_audio_stream_key = None


# Export the handler class
handler_class = SemanticTurnDetectorHandler
