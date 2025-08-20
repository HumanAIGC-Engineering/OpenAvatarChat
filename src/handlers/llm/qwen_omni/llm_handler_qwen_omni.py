import base64
import io
import os
import queue
import threading
import time
from abc import ABC
from typing import Optional, cast, Dict, List

import dashscope
import numpy as np
from PIL import Image
from dashscope.audio.qwen_omni import *
from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.common.handler_base import HandlerBase, HandlerDetail, HandlerBaseInfo, HandlerDataInfo
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry


class QwenOmniConfig(HandlerBaseConfigModel, BaseModel):
    model_name: str = Field(default="qwen-omni-turbo-realtime")  # Qwen-Omni model name
    api_key: str = Field(default=os.getenv("DASHSCOPE_API_KEY"))  # DashScope API key for authentication
    voice: str = Field(default="Chelsie")  # Voice character for audio output
    enable_video_input: bool = Field(default=False)  # Enable video input processing
    enable_text_output: bool = Field(default=False)  # Enable real-time text output streaming
    input_audio_format: str = Field(default="PCM_16000HZ_MONO_16BIT")  # Input audio format specification
    output_audio_format: str = Field(default="PCM_24000HZ_MONO_16BIT")  # Output audio format specification
    enable_turn_detection: bool = Field(default=False)  # Enable server-side turn detection
    enable_input_transcription: bool = Field(default=False)  # Control input audio transcription
    transcription_model: str = Field(default="gummy-realtime-v1")  # Model for audio transcription
    video_frame_interval_ms: int = Field(default=1000, ge=500)  # Video frame sending interval in milliseconds



class QwenOmniContext(HandlerContext):
    """
    Context class for Qwen-Omni handler.
    Manages conversation state, audio/text processing queues and threads, and connection lifecycle.
    """
    def __init__(self, session_id: str):
        super().__init__(session_id)
        
        # ==================== Configuration ====================
        self.config: Optional[QwenOmniConfig] = None
        
        # ==================== Core Conversation ====================
        self.conversation: Optional[OmniRealtimeConversation] = None
        self.callback = None
        self.session_update_params: Optional[Dict] = None  # Cached session params for heartbeat
        
        # ==================== Connection State Management ====================
        self.shutdown_event: threading.Event = threading.Event()
        self.is_connected = False
        self.connection_ready_event = threading.Event()
        
        # ==================== Audio/Text Processing ====================
        # Processing queues
        self.recv_audio_queue = queue.Queue()
        self.recv_text_queue = queue.Queue()
        # Processing threads
        self.audio_processing_thread: Optional[threading.Thread] = None
        self.text_processing_thread: Optional[threading.Thread] = None
        
        # ==================== Turn State Management ====================
        self.current_speech_id: Optional[str] = None
        self.current_turn_audio_started: bool = False
        
        # ==================== Video Processing ====================
        self._last_video_sent_ms: float = 0.0
        
        # ==================== Auto-Reconnection ====================
        self.reconnect_enabled: bool = True  # Enable/disable auto-reconnection
        self.reconnect_attempts: int = 0  # Current reconnect attempt count
        self.max_reconnect_attempts: int = 3  # Maximum reconnect attempts
        # ==================== Reconnection Constants ====================
        self._RECONNECT_DELAY_SECONDS: float = 5.0  # Fixed delay between reconnect attempts
        self._RECONNECT_TIMEOUT_SECONDS: int = 15   # Timeout for connection establishment
        self._SLEEP_INTERVAL_SECONDS: float = 0.5   # Sleep interval for interruptible delays
        self.reconnect_thread: Optional[threading.Thread] = None  # Reconnection thread
        self.is_reconnecting: bool = False  # Reconnection status indicator
        self.last_disconnect_time: float = 0.0  # Last disconnect timestamp for analytics
        
        # ==================== Heartbeat/Keepalive ====================
        self.is_processing = False
        self.heartbeat_interval_sec: int = 25  # Heartbeat interval, default 25s
        self.heartbeat_thread: Optional[threading.Thread] = None
        
        # ==================== Data Definitions Cache ====================
        self.output_definitions: Dict[ChatDataType, DataBundleDefinition] = {}  # Cached for efficiency
        
        # ==================== Debug Features ====================
        self.enable_debug_audio: bool = False  # Control debug audio saving
        self.debug_audio_buffer: List[np.ndarray] = []  # Buffer for debug audio data

    def trigger_reconnection(self) -> None:
        """
        Trigger automatic reconnection process when connection is lost.
        
        Evaluates reconnection conditions and initiates the process if appropriate.
        Implements safeguards to prevent duplicate attempts and respects shutdown.
        """
        # Check if reconnection should be attempted
        if not (self.reconnect_enabled and 
                not self.shutdown_event.is_set() and 
                self.reconnect_attempts < self.max_reconnect_attempts and
                not self.is_reconnecting):
            
            # Log the reason for skipping
            if self.reconnect_attempts >= self.max_reconnect_attempts:
                logger.error(f"Reconnection abandoned: max attempts ({self.max_reconnect_attempts}) exceeded")
            elif self.is_reconnecting:
                logger.debug("Reconnection skipped: already in progress")
            elif not self.reconnect_enabled:
                logger.debug("Reconnection skipped: disabled")
            elif self.shutdown_event.is_set():
                logger.debug("Reconnection skipped: shutdown in progress")
            return
            
        logger.info("Connection lost, initiating reconnection process")
        self._start_reconnection_thread()

    def _start_reconnection_thread(self) -> None:
        """
        Start the reconnection worker thread if conditions allow.
        
        Performs safety checks and ensures only one reconnection thread
        is active at a time.
        """
        # Double-check conditions to prevent race conditions
        if not (self.reconnect_enabled and 
                not self.shutdown_event.is_set() and 
                self.reconnect_attempts < self.max_reconnect_attempts and
                not self.is_reconnecting):
            logger.debug("Reconnection thread start aborted: conditions changed")
            return
            
        # Check if reconnection thread is already running
        if (self.reconnect_thread is not None and self.reconnect_thread.is_alive()):
            logger.debug("Reconnection thread already active, skipping start")
            return
            
        # Create and start new reconnection thread
        self.is_reconnecting = True
        thread_name = f"QwenOmni-Reconnect-{self.session_id[:8]}"
        
        self.reconnect_thread = threading.Thread(
            target=self._reconnection_worker,
            daemon=True,
            name=thread_name
        )
        self.reconnect_thread.start()
        logger.info(f"Reconnection thread '{thread_name}' started")
    


    def _reconnection_worker(self) -> None:
        """
        Worker thread that handles the reconnection process.
        
        This method implements a retry loop with fixed delay between attempts.
        It handles connection establishment, session restoration, and proper
        cleanup on completion or failure.
        
        The worker will continue attempting reconnection until one of:
        - Successful reconnection is established
        - Maximum retry attempts are reached
        - Shutdown is requested
        - Reconnection is disabled
        """
        try:
            logger.info(f"Reconnection worker started (disconnect time: {time.time() - self.last_disconnect_time:.1f}s ago)")
            
            # Loop until successful reconnection or max attempts reached
            while (not self.shutdown_event.is_set() and 
                   self.reconnect_enabled and 
                   self.reconnect_attempts < self.max_reconnect_attempts):
                
                # Apply delay before retry (except for first attempt)
                if self.reconnect_attempts > 0:
                    logger.info(f"Waiting {self._RECONNECT_DELAY_SECONDS:.1f}s before next reconnection attempt")
                    
                    # Interruptible sleep - check shutdown every 0.5s
                    for _ in range(int(self._RECONNECT_DELAY_SECONDS * 2)):
                        if self.shutdown_event.is_set():
                            logger.info("Reconnection aborted: shutdown during delay")
                            return
                        time.sleep(self._SLEEP_INTERVAL_SECONDS)
                else:
                    logger.info("Starting immediate reconnection (first attempt)")
                
                # Final check before attempting reconnection
                if (self.shutdown_event.is_set() or 
                    not self.reconnect_enabled or 
                    self.reconnect_attempts >= self.max_reconnect_attempts):
                    break
                
                # Increment attempt counter
                self.reconnect_attempts += 1
                logger.info(f"Attempting reconnection {self.reconnect_attempts}/{self.max_reconnect_attempts}")
                
                try:
                    # Reset connection state
                    self.is_connected = False
                    self.connection_ready_event.clear()
                    
                    # Close old conversation if exists
                    if self.conversation:
                        try:
                            self.conversation.close()
                        except Exception as close_err:
                            logger.opt(exception=True).debug(f"Error closing old conversation: {close_err}")
                    
                    # Create new conversation instance
                    self.conversation = OmniRealtimeConversation(
                        model=self.config.model_name,
                        callback=self.callback,
                    )
                    
                    # Attempt to connect
                    self.conversation.connect()
                    
                    # Wait for connection establishment
                    if self.connection_ready_event.wait(timeout=self._RECONNECT_TIMEOUT_SECONDS):
                        if self.is_connected:
                            # Reconnection successful
                            reconnect_duration = time.time() - self.last_disconnect_time
                            logger.info(f"Reconnection successful! (duration: {reconnect_duration:.1f}s, attempts: {self.reconnect_attempts})")
                            
                            # Reset reconnect state
                            self.reconnect_attempts = 0
                            self.is_reconnecting = False
                            
                            # Update session with previous parameters
                            if self.session_update_params:
                                try:
                                    self.conversation.update_session(**self.session_update_params)
                                    logger.info("Session updated after reconnection")
                                except Exception as session_err:
                                    logger.opt(exception=True).warning(f"Failed to update session after reconnection: {session_err}")
                            
                            return  # Exit successfully
                        else:
                            logger.error("Connection established but is_connected flag not set")
                    else:
                        logger.error("Timeout waiting for reconnection")
                        
                except Exception as e:
                    logger.opt(exception=True).error(f"Reconnection attempt {self.reconnect_attempts} failed: {e}")
                
                # Log retry information for non-final attempts
                if self.reconnect_attempts < self.max_reconnect_attempts:
                    logger.info(
                        f"Reconnection attempt {self.reconnect_attempts} failed, "
                        f"will retry in {self._RECONNECT_DELAY_SECONDS:.1f}s"
                    )
            
            # Exit: either max attempts reached or shutdown/disabled
            if self.reconnect_attempts >= self.max_reconnect_attempts:
                logger.error(f"All reconnection attempts exhausted. Max attempts: {self.max_reconnect_attempts}")
            elif self.shutdown_event.is_set():
                logger.info("Reconnection aborted due to shutdown")
            elif not self.reconnect_enabled:
                logger.info("Reconnection disabled during process")
                
        except Exception as e:
            logger.opt(exception=True).error(f"Error in reconnection worker: {e}")
        finally:
            # Always clear reconnection flag when worker exits
            self.is_reconnecting = False
            self.reconnect_thread = None
            total_duration = time.time() - self.last_disconnect_time
            logger.info(f"Reconnection worker finished (total duration: {total_duration:.1f}s)")


class QwenOmniCallback(OmniRealtimeCallback):
    """
    Callback handler class for Qwen-Omni realtime events.
    Processes connection events, audio/text deltas, and response completion.
    """
    def __init__(self, context: QwenOmniContext):
        super().__init__()
        self.context = context
        
    def on_open(self) -> None:
        """
        Handle connection open events.
        
        This callback is invoked when the WebSocket connection is successfully
        established. It updates the connection state and signals waiting threads.
        """
        logger.info("Qwen-Omni connection opened successfully")
        self.context.is_connected = True
        self.context.connection_ready_event.set()
        
    def on_close(self, close_status_code, close_msg) -> None:
        """
        Handle connection close events.
        
        This callback is invoked when the WebSocket connection is closed.
        It updates the connection state and triggers reconnection if appropriate.
        
        Args:
            close_status_code: WebSocket close status code
            close_msg: Close message from the server
        """
        logger.info(
            f"Qwen-Omni connection closed: status={close_status_code}, "
            f"message='{close_msg}'"
        )
        
        # Update connection state
        self.context.is_connected = False
        self.context.last_disconnect_time = time.time()
        
        # Trigger reconnection process (with built-in safety checks)
        try:
            self.context.trigger_reconnection()
        except Exception as e:
            logger.opt(exception=True).error(
                f"Error during reconnection trigger: {e}"
            )
        
    def on_event(self, response: str) -> None:
        try:
            event_type = response.get('type')
            # ==================== Core Business Event Processing ====================
            # Log all events except high-frequency delta events
            if event_type not in ['response.audio.delta', 'response.audio_transcript.delta', 'response.text.delta']:
                logger.info(f"OmniRealtimeCallback event: type={event_type}, data={response}")
            
            if event_type == 'error':
                # Server error handling
                error_info = response.get('error', {})
                error_type = error_info.get('type', 'unknown')
                error_code = error_info.get('code', 'unknown')
                error_message = error_info.get('message', 'unknown')
                error_param = error_info.get('param', '')
                logger.error(f"Server error: {error_type} {error_code} - {error_message} (param: {error_param})")
                
            elif event_type == 'conversation.item.input_audio_transcription.completed':
                # Audio transcription completed - output user text if enabled
                transcript = response.get('transcript', '')
                logger.debug(f"Audio transcription completed: {transcript}")
                
                if self.context.config.enable_input_transcription:
                    human_text_def = self.context.output_definitions.get(ChatDataType.HUMAN_TEXT)
                    if human_text_def is not None and transcript:
                        out = DataBundle(human_text_def)
                        out.set_main_data(transcript)
                        out.add_meta("human_text_end", True)
                        # Bind to current turn's speech_id (fallback to session_id if not exists)
                        speech_id = self.context.current_speech_id or self.context.session_id
                        out.add_meta("speech_id", speech_id)
                        chat_data = ChatData(type=ChatDataType.HUMAN_TEXT, data=out)
                        self.context.submit_data(chat_data)
                    
            elif event_type == 'conversation.item.input_audio_transcription.failed':
                # Audio transcription failure handling
                error_info = response.get('error', {})
                error_code = error_info.get('code', 'unknown')
                error_message = error_info.get('message', 'unknown')
                logger.error(f"Audio transcription failed: {error_code} - {error_message}")
                
            elif event_type in ['response.audio_transcript.delta', 'response.text.delta']:
                # Real-time text output
                text_delta = response.get('delta', '')
                if text_delta:
                    logger.debug(f"Text delta: {text_delta}")
                    if self.context.config.enable_text_output:
                        text_item = {
                            'text_content': text_delta,
                            'avatar_text_end': False
                        }
                        self.context.recv_text_queue.put(text_item)
                    
            elif event_type == 'response.audio.delta':
                # Real-time audio output
                audio_b64 = response.get('delta', '')
                if audio_b64:
                    logger.debug(f"Audio delta received: len={len(audio_b64)}")
                    audio_item = {
                        'audio_b64_str': audio_b64,
                        'avatar_speech_end': False
                    }
                    self.context.recv_audio_queue.put(audio_item)
                
            elif event_type == 'response.done':
                # Response completed - add completion markers to queues
                # logger.info(f"Response completed: {response}")
                self.context.is_processing = False
                self._send_completion_markers()
                
            # ==================== Debug and Monitoring Events ====================
            
            elif event_type == 'session.created':
                logger.debug(f"Session created: {response['session']['id']}")
                
            elif event_type == 'session.updated':
                logger.debug(f"Session updated: {response['session']['id']}")
                
            elif event_type == 'input_audio_buffer.speech_started':
                audio_start_ms = response.get('audio_start_ms', 0)
                item_id = response.get('item_id', '')
                logger.debug(f"Speech started: audio_start_ms={audio_start_ms}, item_id={item_id}")
                
            elif event_type == 'input_audio_buffer.speech_stopped':
                audio_end_ms = response.get('audio_end_ms', 0)
                item_id = response.get('item_id', '')
                logger.debug(f"Speech stopped: audio_end_ms={audio_end_ms}, item_id={item_id}")
                
            elif event_type == 'input_audio_buffer.committed':
                item_id = response.get('item_id', '')
                logger.debug(f"Audio buffer committed: item_id={item_id}")
                
            elif event_type == 'response.created':
                response_id = response.get('response', {}).get('id', '')
                logger.debug(f"Response created: response_id={response_id}")
                
            elif event_type == 'response.audio.done':
                response_id = response.get('response_id', '')
                item_id = response.get('item_id', '')
                logger.debug(f"Audio output completed: response_id={response_id}, item_id={item_id}")
                
            elif event_type == 'response.text.done':
                response_id = response.get('response_id', '')
                item_id = response.get('item_id', '')
                text = response.get('text', '')
                logger.debug(f"Text output completed: response_id={response_id}, item_id={item_id}, text_length={len(text)}")
                
            elif event_type == 'response.audio_transcript.done':
                response_id = response.get('response_id', '')
                item_id = response.get('item_id', '')
                part = response.get('part', {})
                text = part.get('text', '')
                logger.debug(f"Audio transcript completed: response_id={response_id}, item_id={item_id}, text={text}")
                
            elif event_type == 'response.output_item.added':
                response_id = response.get('response_id', '')
                output_index = response.get('output_index', 0)
                item = response.get('item', {})
                item_id = item.get('id', '')
                logger.debug(f"Output item added: response_id={response_id}, output_index={output_index}, item_id={item_id}")
                
            elif event_type == 'response.output_item.done':
                response_id = response.get('response_id', '')
                output_index = response.get('output_index', 0)
                item = response.get('item', {})
                item_id = item.get('id', '')
                status = item.get('status', '')
                logger.debug(f"Output item completed: response_id={response_id}, output_index={output_index}, item_id={item_id}, status={status}")
                
            elif event_type == 'response.content_part.added':
                response_id = response.get('response_id', '')
                item_id = response.get('item_id', '')
                content_index = response.get('content_index', 0)
                part = response.get('part', {})
                part_type = part.get('type', '')
                logger.debug(f"Content part added: response_id={response_id}, item_id={item_id}, content_index={content_index}, type={part_type}")
                
            elif event_type == 'response.content_part.done':
                response_id = response.get('response_id', '')
                item_id = response.get('item_id', '')
                content_index = response.get('content_index', 0)
                part = response.get('part', {})
                part_type = part.get('type', '')
                text = part.get('text', '')
                logger.debug(f"Content part completed: response_id={response_id}, item_id={item_id}, content_index={content_index}, type={part_type}, text_length={len(text)}")
                
            elif event_type == 'conversation.item.created':
                item = response.get('item', {})
                item_id = item.get('id', '')
                item_type = item.get('type', '')
                status = item.get('status', '')
                role = item.get('role', '')
                logger.debug(f"Conversation item created: item_id={item_id}, type={item_type}, status={status}, role={role}")
                
            else:
                # Handle unknown or unimplemented event types
                logger.debug(f"Unhandled event type: {event_type}")
                
        except Exception as e:
            logger.opt(exception=True).error(f"Error in callback: {e}")


    def _send_completion_markers(self):
        """
        Send turn completion markers to audio processing queue.
        Ensures proper end-of-speech signaling for both audio and text outputs.
        """
        try:
            speech_id = self.context.current_speech_id
            if not speech_id:
                logger.error(f"No speech_id found for completion markers")
                return
            # Add end markers to audio processing queue, ensuring processing after all audio data
            end_item = {
                'audio_b64_str': None,
                'avatar_speech_end': True,
            }
            self.context.recv_audio_queue.put(end_item)
            logger.debug(f"Queued completion markers for speech_id: {speech_id}")

            # Also add text end marker to queue
            if self.context.config.enable_text_output:
                text_end_item = {
                    'text_content': None,
                    'avatar_text_end': True,
                }
                self.context.recv_text_queue.put(text_end_item)
                logger.debug(f"Queued text completion marker for speech_id: {speech_id}")

            
        except Exception as e:
            logger.opt(exception=True).error(f"Error sending completion markers: {e}")




class HandlerSeq2SeqQwenOmni(HandlerBase, ABC):
    def __init__(self):
        super().__init__()
        self.output_definitions: Dict[ChatDataType, DataBundleDefinition] = {}

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=QwenOmniConfig,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        if isinstance(handler_config, QwenOmniConfig):
            if handler_config.api_key is None or len(handler_config.api_key) == 0:
                error_message = 'DASHSCOPE_API_KEY is required for Qwen-Omni handler'
                logger.error(error_message)
                raise ValueError(error_message)
            
            dashscope.api_key = handler_config.api_key
            logger.info("Qwen-Omni handler loaded successfully")

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[BaseModel] = None) -> HandlerContext:
        """
        Create processing context for the handler.
        Initializes conversation, callback, and context configuration.
        """
        if not isinstance(handler_config, QwenOmniConfig):
            handler_config = QwenOmniConfig()
            
        context = QwenOmniContext(session_context.session_info.session_id)
        context.config = handler_config
        
        context.callback = QwenOmniCallback(context)
    
        context.conversation = OmniRealtimeConversation(
            model=handler_config.model_name,
            callback=context.callback,
        )
        return context

    def start_context(self, session_context, handler_context):

        context = cast(QwenOmniContext, handler_context)
        
        try:
            # Check API key
            if not dashscope.api_key:
                raise ValueError("DashScope API key not set")
            
            # Start audio processing worker thread
            if context.audio_processing_thread is None or not context.audio_processing_thread.is_alive():
                context.audio_processing_thread = threading.Thread(target=self._audio_processing_worker, args=(context,), daemon=True)
                context.audio_processing_thread.start()
            
            # Start text processing worker thread
            if context.text_processing_thread is None or not context.text_processing_thread.is_alive():
                context.text_processing_thread = threading.Thread(target=self._text_processing_worker, args=(context,), daemon=True)
                context.text_processing_thread.start()
            
            # Connect to Qwen-Omni service
            logger.info("Connecting to Qwen-Omni service...")
            context.conversation.connect()
            
            # Wait for connection establishment
            if not context.connection_ready_event.wait(timeout=15):
                raise TimeoutError("Timeout waiting for Qwen-Omni connection")
            
            if not context.is_connected:
                raise ConnectionError("Failed to establish connection to Qwen-Omni service")
            
            output_modalities = [MultiModality.AUDIO, MultiModality.TEXT]
            
            try:
                input_format = getattr(AudioFormat, context.config.input_audio_format)
                output_format = getattr(AudioFormat, context.config.output_audio_format)
            except AttributeError as e:
                logger.opt(exception=True).error(f"Invalid audio format: {e}")
                input_format = AudioFormat.PCM_16000HZ_MONO_16BIT
                output_format = AudioFormat.PCM_24000HZ_MONO_16BIT
                
            session_update_params = dict(
                output_modalities=output_modalities,
                voice=context.config.voice,
                input_audio_format=input_format,
                output_audio_format=output_format,
                enable_input_audio_transcription=context.config.enable_input_transcription,
                input_audio_transcription_model=context.config.transcription_model,
                enable_turn_detection=context.config.enable_turn_detection,
            )
            context.session_update_params = session_update_params
            context.conversation.update_session(**session_update_params)
            
            # Reset reconnection state after successful initial connection
            context.reconnect_attempts = 0
            context.is_reconnecting = False
            
            # Start heartbeat thread for periodic session.update (only when connection alive and not generating)
            if context.heartbeat_thread is None or not context.heartbeat_thread.is_alive():
                context.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, args=(context,), daemon=True)
                context.heartbeat_thread.start()

            logger.info(f"Qwen-Omni context started successfully for session {context.session_id}")  
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to start Qwen-Omni context: {e}")
            try:
                if context.conversation is not None:
                    context.conversation.close()
            except Exception as cleanup_err:
                logger.opt(exception=True).warning(f"Error closing Qwen-Omni conversation: {cleanup_err}")
            finally:
                context.is_connected = False
                context.is_processing = False
            raise RuntimeError(f"Qwen-Omni context startup failed: {e}") from e

    def _heartbeat_loop(self, context: QwenOmniContext):
        interval = max(20, int(context.heartbeat_interval_sec or 25))
        while not context.shutdown_event.is_set():
            time.sleep(interval)
            if context.shutdown_event.is_set():
                break
            # Only send heartbeat when connection is alive and not generating
            if context.is_connected and (not context.is_processing) and context.session_update_params is not None:
                try:
                    context.conversation.update_session(**context.session_update_params)
                    logger.debug("Sent heartbeat session.update")
                except Exception as e:
                    logger.opt(exception=True).warning(f"Heartbeat failed: {e}")

    def _audio_processing_worker(self, context: QwenOmniContext):
        logger.info("Audio processing worker thread started")
        while not context.shutdown_event.is_set():
            try:
                queue_item = context.recv_audio_queue.get(timeout=1.0)
                
                if queue_item.get('avatar_speech_end', False) == True:
                    speech_id = context.current_speech_id
                    if speech_id:
                        audio_def = context.output_definitions.get(ChatDataType.AVATAR_AUDIO)
                        if audio_def:
                            end_audio = DataBundle(audio_def)
                            end_audio.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
                            end_audio.add_meta("avatar_speech_end", True)
                            end_audio.add_meta("speech_id", speech_id)
                            end_audio_chat = ChatData(type=ChatDataType.AVATAR_AUDIO, data=end_audio)
                            context.submit_data(end_audio_chat)
                        
                        context.current_speech_id = None
                        logger.debug(f"Sent audio completion marker for speech_id: {speech_id}")
                    continue
                
                # Process audio data
                audio_b64_str = queue_item.get('audio_b64_str')
                if not audio_b64_str:
                    continue
                
                # Decode base64 audio data
                audio_bytes = base64.b64decode(audio_b64_str)
                
                # Check if audio data is empty
                if len(audio_bytes) == 0:
                    logger.error("Received empty audio data")
                    continue
                
                # Check if audio data length is aligned to int16
                if len(audio_bytes) % 2 != 0:
                    logger.error(f"Audio data length is not aligned to int16: {len(audio_bytes)} bytes (should be even)")
                    continue
                
                # Log audio data length information
                audio_samples = len(audio_bytes) // 2  # int16 = 2 bytes
                audio_duration_ms = (audio_samples / 24000) * 1000  # 24kHz sample rate
                audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32767.0
                logger.debug(
                    f"Processing audio chunk: {len(audio_bytes)} bytes, {audio_samples} samples, {audio_duration_ms:.1f}ms | "
                    f"Audio array: shape={audio_array.shape}, min={audio_array.min():.4f}, max={audio_array.max():.4f}, mean={audio_array.mean():.4f}"
                )
                
                # Ensure audio data format is correct (1, N) for output
                if audio_array.ndim == 1:
                    audio_array = audio_array[np.newaxis, ...]
                
                try:
                    output_definition = context.output_definitions.get(ChatDataType.AVATAR_AUDIO)
                    # Use session_id as default speech_id to ensure always have valid identifier
                    speech_id = context.current_speech_id or context.session_id
                    
                    # Create output data bundle and wrap as ChatData
                    output = DataBundle(output_definition)
                    output.set_main_data(audio_array)
                    output.add_meta("speech_id", speech_id)
                    output.add_meta("avatar_speech_end", False)
                    chat_data = ChatData(type=ChatDataType.AVATAR_AUDIO, data=output)
                    
                    logger.debug(f"Submitting audio: shape={audio_array.shape}, speech_id={speech_id}")
                    context.submit_data(chat_data)
                    
                except Exception as e:
                    logger.opt(exception=True).error(f"Error submitting audio: {e}")
                    # Log error but don't cache, avoiding complex recovery logic
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.opt(exception=True).error(f"Error in audio processing worker: {e}")
        
        logger.info("Audio processing worker thread stopped")

    def _text_processing_worker(self, context: QwenOmniContext):
        logger.info("Text processing worker thread started")
        while not context.shutdown_event.is_set():
            try:
                queue_item = context.recv_text_queue.get(timeout=1.0)
                
                if queue_item.get('avatar_text_end', False):
                    speech_id = context.current_speech_id
                    if speech_id:
                        text_def = context.output_definitions.get(ChatDataType.AVATAR_TEXT)
                        if text_def:
                            end_text = DataBundle(text_def)
                            end_text.set_main_data("")
                            end_text.add_meta("avatar_text_end", True)
                            end_text.add_meta("speech_id", speech_id)
                            end_text_chat = ChatData(type=ChatDataType.AVATAR_TEXT, data=end_text)
                            context.submit_data(end_text_chat)
                        logger.debug(f"Sent text completion marker for speech_id: {speech_id}")
                    continue
                
                # Process text data
                text_content = queue_item.get('text_content')
                if not text_content:
                    continue
                
                try:
                    text_def = context.output_definitions.get(ChatDataType.AVATAR_TEXT)
                    speech_id = context.current_speech_id or context.session_id
                    
                    # Create text output data bundle
                    output = DataBundle(text_def)
                    output.set_main_data(text_content)
                    output.add_meta("speech_id", speech_id)
                    output.add_meta("avatar_text_end", False)
                    
                    logger.debug(f"Submitting text output: {text_content}")
                    chat_data = ChatData(type=ChatDataType.AVATAR_TEXT, data=output)
                    context.submit_data(chat_data)
                    
                except Exception as e:
                    logger.opt(exception=True).error(f"Error submitting text: {e}")
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.opt(exception=True).error(f"Error in text processing worker: {e}")
        
        logger.info("Text processing worker thread stopped")

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        # Initialize output definitions once, stored in handler for session sharing
        if not self.output_definitions:
            audio_def = DataBundleDefinition()
            audio_def.add_entry(DataBundleEntry.create_audio_entry("avatar_audio", 1, 24000))
            text_def = DataBundleDefinition()
            text_def.add_entry(DataBundleEntry.create_text_entry("avatar_text"))
            human_text_def = DataBundleDefinition()
            human_text_def.add_entry(DataBundleEntry.create_text_entry("human_text"))
            self.output_definitions = {
                ChatDataType.HUMAN_TEXT: human_text_def,
                ChatDataType.AVATAR_AUDIO: audio_def,
                ChatDataType.AVATAR_TEXT: text_def,
            }

        inputs = {
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
            ),
            ChatDataType.CAMERA_VIDEO: HandlerDataInfo(
                type=ChatDataType.CAMERA_VIDEO,
            ),
        }

        outputs = {
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(
                type=ChatDataType.HUMAN_TEXT,
                definition=self.output_definitions[ChatDataType.HUMAN_TEXT],
            ),
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                definition=self.output_definitions[ChatDataType.AVATAR_AUDIO],
            ),
            ChatDataType.AVATAR_TEXT: HandlerDataInfo(
                type=ChatDataType.AVATAR_TEXT,
                definition=self.output_definitions[ChatDataType.AVATAR_TEXT],
            ),
        }

        # Callback still references through context, but points directly to handler-level definitions to avoid copying
        ctx = cast(QwenOmniContext, context)
        ctx.output_definitions = self.output_definitions
        return HandlerDetail(inputs=inputs, outputs=outputs)

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        context = cast(QwenOmniContext, context)
        
        if inputs.type == ChatDataType.HUMAN_AUDIO:
            self._handle_audio_input(context, inputs)
        elif inputs.type == ChatDataType.CAMERA_VIDEO and context.config.enable_video_input:
            self._handle_video_input(context, inputs)
        


    def _handle_audio_input(self, context: QwenOmniContext, inputs: ChatData):
        """
        Process audio input.
        Handles audio data conversion, sends to Qwen-Omni, and manages turn lifecycle.
        """
        audio_data = inputs.data.get_main_data()
        if audio_data is None:
            return
            
        # Get speech_id for tracking
        speech_id = inputs.data.get_meta("speech_id")
        if speech_id is None:
            speech_id = context.session_id
            
        # Set current_speech_id when starting audio processing to ensure real-time handling
        if context.current_speech_id is None:
            context.current_speech_id = speech_id
            
        # Convert audio format and send
        if audio_data is not None:
            # Ensure audio is in correct format (16kHz, mono, int16)
            if audio_data.dtype != np.int16:
                # If float32 format, convert to int16
                if audio_data.dtype == np.float32:
                    audio_data = np.clip(audio_data, -1.0, 1.0)
                    audio_data = (audio_data * 32767).astype(np.int16)
                else:
                    audio_data = audio_data.astype(np.int16)
            
            # Debug: Save audio data for debugging if enabled
            if context.enable_debug_audio:
                context.debug_audio_buffer.append(audio_data.copy())
            
            # Convert to bytes and encode as base64
            audio_bytes = audio_data.tobytes()
            audio_b64 = base64.b64encode(audio_bytes).decode('ascii')
            

            context.conversation.append_audio(audio_b64)
            # Mark that this turn has started audio
            if not context.current_turn_audio_started:
                context.current_turn_audio_started = True

            
        # Check if this is speech end
        speech_end = inputs.data.get_meta("human_speech_end", False)
        if speech_end:
            # Set current turn identifier
            context.current_speech_id = speech_id
            
            # Debug: Save complete audio file when speech ends if enabled
            if context.enable_debug_audio:
                self._save_debug_audio(context, speech_id)
            
            # Commit audio and create response
            context.conversation.commit()
            try:
                context.conversation.create_response()
                context.is_processing = True  # Set only after successful response creation
            except Exception as e:
                logger.opt(exception=True).error(f"Failed to create response: {e}")
                # Keep is_processing as False if response creation failed
            # End this turn, reset audio start marker
            context.current_turn_audio_started = False
    
    def _save_debug_audio(self, context: QwenOmniContext, speech_id: str):
        """
        Save concatenated audio buffer to file for debugging.
        """
        if not context.enable_debug_audio:
            return
            
        if not context.debug_audio_buffer:
            logger.warning(f"No audio data to save for speech_id: {speech_id}")
            return
            
        try:
            import os
            import wave
            from datetime import datetime
            
            # Create debug directory
            debug_dir = "logs/debug_audio"
            os.makedirs(debug_dir, exist_ok=True)
            
            # Concatenate all audio chunks
            if len(context.debug_audio_buffer) == 1:
                complete_audio = context.debug_audio_buffer[0]
            else:
                complete_audio = np.concatenate(context.debug_audio_buffer, axis=None)
            
            # Ensure audio is int16 format for WAV
            if complete_audio.dtype != np.int16:
                complete_audio = complete_audio.astype(np.int16)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"debug_audio_{speech_id}_{timestamp}.wav"
            filepath = os.path.join(debug_dir, filename)
            
            # Save as WAV file (16kHz, mono, 16-bit)
            with wave.open(filepath, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit = 2 bytes
                wav_file.setframerate(16000)  # 16kHz
                wav_file.writeframes(complete_audio.tobytes())
            
            logger.info(f"💾 Saved debug audio: {filepath} (duration: {len(complete_audio)/16000:.2f}s, {len(context.debug_audio_buffer)} chunks)")
            
            # Clear buffer for next speech
            context.debug_audio_buffer.clear()
            
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to save debug audio: {e}")
            # Clear buffer even if save failed
            context.debug_audio_buffer.clear()


    def _process_video_frame(self, video_frame: np.ndarray) -> Optional[str]:
        """
        Process video frame to base64 JPEG string.
        
        Converts BGR format (default camera output) to RGB format
        for proper color processing.
        """
        try:
            # Remove batch dimension and ensure 3D array
            frame_array = np.squeeze(video_frame)
            
            # Validate frame format (H, W, 3)
            if frame_array.ndim != 3 or frame_array.shape[-1] != 3:
                return None
            
            # Convert to uint8 if needed (assume float[0,1] range)
            if frame_array.dtype != np.uint8:
                frame_array = (np.clip(frame_array, 0.0, 1.0) * 255.0).astype(np.uint8)
            
            # Convert BGR to RGB (camera default format to RGB)
            # OpenCV uses BGR format, PIL uses RGB format
            frame_array_rgb = frame_array[:, :, ::-1]  # Reverse the color channels
            
            # Convert to JPEG and encode as base64
            image = Image.fromarray(frame_array_rgb, mode='RGB')
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=75, optimize=True)
            
            return base64.b64encode(buffer.getvalue()).decode('ascii')
            
        except Exception as e:
            logger.opt(exception=True).error(f"Error processing video frame: {e}")
            return None
        

        
    def _handle_video_input(self, context: QwenOmniContext, inputs: ChatData):
        """
        Process video input and send directly if conditions are met.
        Ensures audio-first constraint and FPS throttling.
        """
        # Check if video input is enabled
        if not context.config.enable_video_input:
            return
        
        video_frame = inputs.data.get_main_data()
        if video_frame is None:
            return
        
        # Check if audio has been sent first (audio-first constraint from docs)
        if not context.current_turn_audio_started:
            logger.debug("Skipping video: audio not started yet (audio-first constraint)")
            return
        
        # Throttle video sending based on FPS interval
        current_time_ms = time.time() * 1000.0
        time_since_last_sent = current_time_ms - context._last_video_sent_ms
        if time_since_last_sent < context.config.video_frame_interval_ms:
            logger.debug(f"Skipping video: throttling (last sent {time_since_last_sent:.0f}ms ago)")
            return
        
        # Process and send the video frame directly
        processed_b64 = self._process_video_frame(video_frame)
        if processed_b64:
            try:
                context.conversation.append_video(processed_b64)
                context._last_video_sent_ms = current_time_ms
                logger.debug(f"📹 Sent video frame directly from handle_video_input")
                
            except Exception as e:
                logger.opt(exception=True).error(f"Error sending video frame: {e}")
        else:
            logger.debug("Failed to process video frame, skipping send")



    def destroy_context(self, context: HandlerContext):
        """
        Destroy context and clean up resources.
        Stops all threads, closes connections, and clears processing queues.
        """
        context = cast(QwenOmniContext, context)
        
        try:
            # Set flags to stop processing
            context.is_processing = False
            context.shutdown_event.set()
            
            # Disable reconnection during shutdown
            context.reconnect_enabled = False
            context.is_reconnecting = False
            
            # Clean up events
            if hasattr(context, 'connection_ready_event'):
                context.connection_ready_event.set()

            # Close connection
            if context.conversation and context.is_connected:
                context.conversation.close()
                context.is_connected = False
                
            # Clear audio processing queue
            while not context.recv_audio_queue.empty():
                try:
                    context.recv_audio_queue.get_nowait()
                except queue.Empty:
                    break
            
            # Clear text processing queue
            while not context.recv_text_queue.empty():
                try:
                    context.recv_text_queue.get_nowait()
                except queue.Empty:
                    break
            
            # Wait for heartbeat thread to finish
            try:
                if context.heartbeat_thread and context.heartbeat_thread.is_alive():
                    context.heartbeat_thread.join(timeout=2)
            except Exception as e:
                logger.opt(exception=True).debug(f"Error while joining heartbeat thread: {e}")
            
            # Wait for audio processing thread to finish
            try:
                if context.audio_processing_thread and context.audio_processing_thread.is_alive():
                    context.audio_processing_thread.join(timeout=2)
            except Exception as e:
                logger.opt(exception=True).debug(f"Error while joining audio processing thread: {e}")
            
            # Wait for text processing thread to finish
            try:
                if context.text_processing_thread and context.text_processing_thread.is_alive():
                    context.text_processing_thread.join(timeout=2)
            except Exception as e:
                logger.opt(exception=True).debug(f"Error while joining text processing thread: {e}")
            
            # Wait for reconnection thread to finish
            try:
                if context.reconnect_thread and context.reconnect_thread.is_alive():
                    logger.debug("Waiting for reconnection thread to finish...")
                    context.reconnect_thread.join(timeout=2)
                    if context.reconnect_thread.is_alive():
                        logger.warning("Reconnection thread did not finish within timeout")
                # Clear thread reference
                context.reconnect_thread = None
            except Exception as e:
                logger.debug(f"Error while joining reconnection thread: {e}")

            
            logger.info(f"Qwen-Omni context destroyed for session {context.session_id}")
            
        except Exception as e:
            logger.opt(exception=True).error(f"Error destroying context: {e}")
