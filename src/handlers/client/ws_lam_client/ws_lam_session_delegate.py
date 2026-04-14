"""
LAM WebSocket Session Delegate

Inherits all ws_client protocol handling from WsInputSessionDelegate.

Supports two upstream modes (set by the handler after creation):

  - ``rtc``: Audio/video upstream goes through WebRTC; this delegate only
    handles the WebSocket downstream (motion data, text echo, signals) and
    minimal upstream commands (Heartbeat, Interrupt, EndSpeech).
  - ``ws``: Pure WebSocket mode — audio input, text input, and all output
    (motion data, audio, text, signals) travel over a single WS connection.

RTC-mode specifics:
  - VIDEO output queue must exist (even if unused) to prevent a tight loop
    in RtcStream.video_emit() that would starve the event loop.
  - Audio output is NOT sent over WS; playback goes through RTC.
  - Text output uses a dedicated queue to avoid competition with the
    RTC data-channel's process_chat_history task.
"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Literal, Optional, Tuple, Union

import numpy as np
from loguru import logger

from chat_engine.data_models.engine_channel_type import EngineChannelType
from handlers.client.ws_client.ws_input_delegate import WsInputSessionDelegate

if TYPE_CHECKING:
    from handlers.client.ws_client.ws_input_delegate import ConnectionInfo


class WsLamClientSessionDelegate(WsInputSessionDelegate):

    def __init__(self, heartbeat_timeout: float = 30.0):
        super().__init__(heartbeat_timeout=heartbeat_timeout)

        self.upstream_mode: Literal["rtc", "ws"] = "rtc"

        # RTC-mode queues (cheap to create; conditionally used at runtime).
        # VIDEO queue: prevents hot-loop in RtcStream.video_emit().
        self.output_queues[EngineChannelType.VIDEO] = asyncio.Queue()
        # Dedicated text queue: avoids RTC data-channel stealing from TEXT queue.
        self.ws_text_queue: asyncio.Queue = asyncio.Queue()

    # ------------------------------------------------------------------
    # Override put_data to echo loopback text via WebSocket
    # ------------------------------------------------------------------

    def put_data(self, modality: EngineChannelType, data: Union[np.ndarray, str],
                 timestamp: Optional[Tuple[int, int]] = None,
                 samplerate: Optional[int] = None,
                 loopback: bool = False,
                 speech_id: Optional[str] = None):
        """
        RTC-mode override for TEXT loopback.

        In RTC mode, text typed by the user enters via the RTC data channel
        and is submitted to the engine with loopback=True.  The engine will
        NOT route HUMAN_TEXT back to this handler (same-source skip), so the
        WebSocket echo would be lost.

        For TEXT with loopback we:
          1. Submit to the engine (same as parent).
          2. Put the ChatData into ws_text_queue (for WebSocket echo)
             INSTEAD of output_queues[TEXT] (which process_chat_history reads).

        In WS mode, text comes via WS SendHumanText and is handled by the
        base class directly — no loopback override needed.
        """
        if self.upstream_mode == "rtc" and loopback and modality == EngineChannelType.TEXT:
            from chat_engine.data_models.chat_data.chat_data_model import ChatData
            from chat_engine.data_models.runtime_data.data_bundle import DataBundle

            if timestamp is None:
                timestamp = self.get_timestamp()
            if self.data_submitter is None:
                return

            definition = self.input_data_definitions.get(modality)
            chat_data_type = self.modality_mapping.get(modality)
            if chat_data_type is None or definition is None:
                return

            data_bundle = DataBundle(definition)
            data_bundle.set_main_data(data)

            chat_data = ChatData(
                source="client",
                type=chat_data_type,
                data=data_bundle,
                timestamp=timestamp,
            )
            self.data_submitter.submit(chat_data, finish_stream=True)
            self.ws_text_queue.put_nowait(chat_data)
            return

        super().put_data(modality, data, timestamp, samplerate, loopback, speech_id)

    # ------------------------------------------------------------------
    # Override clear_data to preserve WebSocket connections
    # ------------------------------------------------------------------

    def clear_data(self):
        """
        In RTC mode, RtcStream.emit() calls clear_data() on first audio
        frame.  The parent implementation clears connection_infos, which
        destroys the active WebSocket connection.  Override to only clear
        queues/buffers while preserving WS connection state.

        In WS mode there is no RtcStream, so clear_data() is only called
        from destroy_context.  Delegating to the parent is safe.
        """
        if self.upstream_mode == "rtc":
            for data_queue in self.output_queues.values():
                while not data_queue.empty():
                    try:
                        data_queue.get_nowait()
                    except Exception:
                        pass
            while not self.ws_text_queue.empty():
                try:
                    self.ws_text_queue.get_nowait()
                except Exception:
                    pass
            self.text_buffer.clear()
            self.binary_stream_assembler.clear()
            self._active_playback_stream_keys.clear()
            self._cancelled_stream_keys.clear()
        else:
            super().clear_data()

    # ------------------------------------------------------------------
    # Override primary-connection lifecycle
    # ------------------------------------------------------------------

    async def _serve_primary_connection(self, info: ConnectionInfo) -> bool:
        """
        LAM mode primary connection.

        Task set depends on ``upstream_mode``:
          - **rtc**: text via ``_lam_ws_text_output_task`` (dedicated queue),
            no ``_ws_audio_output_task`` (audio goes through RTC).
          - **ws**: standard ``_ws_text_output_task`` and
            ``_ws_audio_output_task`` (everything over WebSocket).

        Motion data, heartbeat, signals, and input are always present.
        """
        self.quit.clear()
        self.motion_welcome_sent = False
        self.motion_welcome_payload = None
        self.binary_stream_assembler.clear()
        self.subscriptions = set(self.AVAILABLE_SUBSCRIPTIONS)

        self.audio_format = "PCM"
        self.audio_sample_rate = 16000
        self.audio_channels = 1
        self._opus_encoder = None
        self._opus_decoder = None

        self.primary_tasks = [
            asyncio.create_task(self._ws_input_task(info)),
            asyncio.create_task(self._ws_motion_output_task()),
            asyncio.create_task(self._heartbeat_monitor_task(info)),
            asyncio.create_task(self._ws_signal_output_task()),
        ]

        if self.upstream_mode == "rtc":
            self.primary_tasks.append(
                asyncio.create_task(self._lam_ws_text_output_task())
            )
        else:
            self.primary_tasks.append(
                asyncio.create_task(self._ws_text_output_task())
            )
            self.primary_tasks.append(
                asyncio.create_task(self._ws_audio_output_task())
            )

        try:
            done, pending = await asyncio.wait(
                self.primary_tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)
        finally:
            for task in self.primary_tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*self.primary_tasks, return_exceptions=True)
            self.primary_tasks = []
            self.quit.set()
            await self._close_all_connections()
            self.motion_welcome_sent = False
            self.motion_welcome_payload = None
            self.binary_stream_assembler.clear()
            logger.info(f"LAM primary connection closed, session={self.session_id}")
        return True

    # ------------------------------------------------------------------
    # Text output — reads from the dedicated ws_text_queue
    # ------------------------------------------------------------------

    async def _lam_ws_text_output_task(self):
        """
        Send text echo over WebSocket.

        Same logic as the parent _ws_text_output_task, but reads from
        self.ws_text_queue so that the RTC data-channel task cannot
        steal items from the shared TEXT output queue.
        """
        from uuid import uuid4
        from chat_engine.data_models.chat_data_type import ChatDataType
        from handlers.client.ws_client.ws_message_protocol import (
            EchoHumanText, EchoAvatarText, MessageHeader, EchoTextPayload,
        )

        logger.info(f"LAM text output task started for session {self.session_id}")

        while not self.quit.is_set():
            try:
                chat_data = await asyncio.wait_for(
                    self.ws_text_queue.get(),
                    timeout=0.1,
                )
            except asyncio.TimeoutError:
                continue

            if chat_data is None or chat_data.data is None:
                continue

            try:
                text = chat_data.data.get_main_data()
                stream_key_str = (
                    chat_data.stream_id.stream_key_str if chat_data.stream_id else None
                )

                if chat_data.type == ChatDataType.HUMAN_TEXT:
                    if "human_text" not in self.subscriptions:
                        continue
                    text_end = chat_data.is_last_data
                    stream_metadata = self._extract_stream_metadata(
                        chat_data, excluded_keys={"human_text_end"},
                    )
                    response = EchoHumanText(
                        header=MessageHeader(name="EchoHumanText", request_id=str(uuid4())),
                        payload=EchoTextPayload(
                            stream_key=stream_key_str,
                            mode="full_text",
                            text=text,
                            end_of_speech=text_end,
                            metadata=stream_metadata,
                        ),
                    )
                    await self._broadcast_message(response)
                    logger.debug(f"LAM echo human text (end={text_end}): {text[:50]}")
                    self.last_human_text = text if not text_end else None

                elif chat_data.type == ChatDataType.AVATAR_TEXT:
                    if "avatar_text" not in self.subscriptions:
                        continue
                    text_end = chat_data.is_last_data
                    stream_metadata = self._extract_stream_metadata(
                        chat_data, excluded_keys={"avatar_text_end"},
                    )
                    response = EchoAvatarText(
                        header=MessageHeader(name="EchoAvatarText", request_id=str(uuid4())),
                        payload=EchoTextPayload(
                            stream_key=stream_key_str,
                            mode="increment",
                            text=text,
                            end_of_speech=text_end,
                            metadata=stream_metadata,
                        ),
                    )
                    await self._broadcast_message(response)
                    logger.debug(f"LAM echo avatar text (end={text_end}): {text[:50]}")

            except Exception as e:
                logger.error(f"Error in LAM text output task for session {self.session_id}: {e}")
                break

        logger.info(f"LAM text output task ended for session {self.session_id}")
