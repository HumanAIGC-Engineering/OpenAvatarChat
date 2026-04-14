import threading
import time
from typing import Dict, Optional
from loguru import logger
import numpy as np
from multiprocessing import shared_memory

from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SharedStates
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.engine_channel_type import EngineChannelType
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from handlers.avatar.liteavatar.liteavatar_worker import LiteAvatarWorker, Tts2FaceEvent
from handlers.avatar.liteavatar.shared_memory_buffer_pool import SharedMemoryDataPacket


class HandlerTts2FaceContext(HandlerContext):
    def __init__(self,
                 session_id: str,
                 lite_avatar_worker: LiteAvatarWorker,
                 shared_status):
        super().__init__(session_id)
        self.lite_avatar_worker: LiteAvatarWorker = lite_avatar_worker
        self.shared_state: SharedStates = shared_status

        self.output_data_definitions: Dict[ChatDataType, DataBundleDefinition] = {}
        
        self.media_out_thread: threading.Thread = None
        self.event_out_thread: threading.Thread = None

        self._current_tts_stream_key: str = None
        self._playback_streamer = None

        self.loop_running = True
        self.media_out_thread = threading.Thread(target=self._media_out_loop)
        self.media_out_thread.start()
        self.event_out_thread = threading.Thread(target=self._event_out_loop)
        self.event_out_thread.start()

    def get_playback_streamer(self):
        """Lazily create a CLIENT_PLAYBACK lifecycle streamer."""
        if self._playback_streamer is None and self.stream_manager is not None:
            self._playback_streamer = self.stream_manager.create_lifecycle_streamer(
                data_type=ChatDataType.CLIENT_PLAYBACK,
                producer_name="LiteAvatar",
                config=ChatStreamConfig(cancelable=False),
            )
        return self._playback_streamer

    def return_data(self, data, chat_data_type: ChatDataType):
        definition = self.output_data_definitions.get(chat_data_type)
        if definition is None:
            return
        data_bundle = DataBundle(definition)
        if chat_data_type.channel_type == EngineChannelType.AUDIO:
            data_bundle.set_main_data(data.squeeze()[np.newaxis, ...])
        elif chat_data_type.channel_type == EngineChannelType.VIDEO:
            data_bundle.set_main_data(data[np.newaxis, ...])
        else:
            return
        chat_data = ChatData(type=chat_data_type, data=data_bundle)
        self.submit_data(chat_data)

    def _media_out_loop(self):
        while self.loop_running:
            no_output = True
            
            # Process audio
            try:
                packet: SharedMemoryDataPacket = self.lite_avatar_worker.audio_out_queue.get_nowait()
                no_output = False
                shm = None
                try:
                    shm = shared_memory.SharedMemory(name=packet.shm_name)
                    audio = np.ndarray(
                        packet.shape,
                        dtype=np.dtype(packet.dtype),
                        buffer=shm.buf[:packet.data_size]
                    ).copy()
                    shm.close()
                    shm = None
                    
                    self.return_data(audio, ChatDataType.AVATAR_AUDIO)
                except Exception as e:
                    import traceback
                    logger.error(f"Error processing audio: {e.__class__.__name__}: {e}")
                    logger.error(f"Packet: idx={packet.buffer_index}, name={packet.shm_name}, shape={packet.shape}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    if shm is not None:
                        try:
                            shm.close()
                        except:
                            pass
                finally:
                    try:
                        self.lite_avatar_worker.shm_pool.release_audio_buffer(packet.buffer_index)
                    except Exception as e:
                        logger.error(f"Error releasing audio buffer: {e}")
            except:
                pass  # Queue empty
            
            # Process video
            try:
                packet: SharedMemoryDataPacket = self.lite_avatar_worker.video_out_queue.get_nowait()
                no_output = False
                shm = None
                try:
                    shm = shared_memory.SharedMemory(name=packet.shm_name)
                    video = np.ndarray(
                        packet.shape,
                        dtype=np.dtype(packet.dtype),
                        buffer=shm.buf[:packet.data_size]
                    ).copy()
                    shm.close()
                    shm = None
                    
                    self.return_data(video, ChatDataType.AVATAR_VIDEO)
                except Exception as e:
                    import traceback
                    logger.error(f"Error processing video: {e.__class__.__name__}: {e}")
                    logger.error(f"Packet: idx={packet.buffer_index}, name={packet.shm_name}, shape={packet.shape}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    if shm is not None:
                        try:
                            shm.close()
                        except:
                            pass
                finally:
                    try:
                        self.lite_avatar_worker.shm_pool.release_video_buffer(packet.buffer_index)
                    except Exception as e:
                        logger.error(f"Error releasing video buffer: {e}")
            except:
                pass  # Queue empty
            
            if no_output:
                time.sleep(0.05)
                continue
        logger.info("media out loop exit")

    def _event_out_loop(self):
        while self.loop_running:
            try:
                event: Tts2FaceEvent = self.lite_avatar_worker.event_out_queue.get(timeout=0.1)
                logger.info("receive output event: {}", event)
                if event == Tts2FaceEvent.SPEAKING_TO_LISTENING:
                    # Close the CLIENT_PLAYBACK lifecycle stream
                    # This auto-emits STREAM_END signal and auto-records to SessionHistory
                    streamer = self.get_playback_streamer()
                    if streamer is not None and self._current_tts_stream_key:
                        streamer.finish_current()
                        logger.info(f"LiteAvatar: CLIENT_PLAYBACK stream closed for stream_key={self._current_tts_stream_key}")
                    self._current_tts_stream_key = None
            except Exception:
                continue
        logger.info("event out loop exit")
    
    def interrupt(self):
        """打断当前语音播放，清空队列并通知子进程"""
        logger.info("LiteAvatar interrupt: clearing output queues and notifying worker")
        # CLIENT_PLAYBACK stream 由引擎的 forward_cancel_signal 级联自动取消，
        # 此处只需清理追踪状态（防止 _event_out_loop 后续重复 finish）
        self._current_tts_stream_key = None
        # 清空音频和视频输出队列
        while not self.lite_avatar_worker.audio_out_queue.empty():
            try:
                packet = self.lite_avatar_worker.audio_out_queue.get_nowait()
                try:
                    self.lite_avatar_worker.shm_pool.release_audio_buffer(packet.buffer_index)
                except:
                    pass
            except:
                break
        while not self.lite_avatar_worker.video_out_queue.empty():
            try:
                packet = self.lite_avatar_worker.video_out_queue.get_nowait()
                try:
                    self.lite_avatar_worker.shm_pool.release_video_buffer(packet.buffer_index)
                except:
                    pass
            except:
                break
        # 通知子进程清空音频处理队列
        self.lite_avatar_worker.event_in_queue.put_nowait(Tts2FaceEvent.INTERRUPT)
        logger.info("LiteAvatar interrupt: done")

    def clear(self):
        logger.info("clear tts2face context")
        self.loop_running = False
        self.lite_avatar_worker.event_in_queue.put_nowait(Tts2FaceEvent.STOP)
        self.media_out_thread.join()
        self.event_out_thread.join()
        self.lite_avatar_worker.release()