import weakref
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union, Tuple, Optional

import gradio
import numpy as np
from fastapi import FastAPI
from loguru import logger

from chat_engine.common.engine_channel_type import EngineChannelType
from chat_engine.common.handler_base import HandlerBase
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.session_info_data import SessionInfoData


class ClientSessionDelegate(ABC):
    @abstractmethod
    async def get_data(self, modality: EngineChannelType, timeout: Optional[float] = 0.1) -> Optional[ChatData]:
        pass

    @abstractmethod
    def put_data(self, modality: EngineChannelType, data: Union[np.ndarray, str],
                 timestamp: Optional[Tuple[int, int]] = None,
                 samplerate: Optional[int] = None, loopback: bool = False):
        pass

    @abstractmethod
    def get_timestamp(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def emit_signal(self, signal: ChatSignal):
        pass

    @abstractmethod
    def clear_data(self):
        pass


class ClientHandlerDelegate:
    def __init__(self, engine_ref, client_handler):
        self.engine_ref = engine_ref
        self.client_handler_ref = weakref.ref(client_handler)

        self.session_delegates = {}

    def start_session(self, session_id: str, **kwargs) -> ClientSessionDelegate:
        logger.info(f"Starting session {session_id}")
        engine = self.engine_ref()
        handler = self.client_handler_ref()
        assert engine is not None
        assert handler is not None

        kwargs["session_id"] = session_id
        session_info = SessionInfoData.model_validate(kwargs)

        session, handler_env = engine.create_client_session(session_info, handler)
        session.start()
        if handler_env.handler_info.client_session_delegate_class is None:
            msg = f"Client handler {handler_env.handler_info.handler_name} does not provide a session delegate."
            raise RuntimeError(msg)
        session_delegate = handler_env.handler_info.client_session_delegate_class()
        handler_env.handler.on_setup_session_delegate(session.session_context, handler_env.context, session_delegate)
        self.session_delegates[session_id] = session_delegate
        return session_delegate

    def stop_session(self, session_id: str):
        engine = self.engine_ref()
        assert engine is not None
        engine.stop_session(session_id)
        self.session_delegates.pop(session_id)

    def find_session_delegate(self, session_id: str):
        return self.session_delegates.get(session_id)


@dataclass
class ClientHandlerInfo:
    session_delegate_class: type[ClientSessionDelegate]


class ClientHandlerBase(HandlerBase, ABC):
    def __init__(self):
        super().__init__()
        self.handler_delegate = ClientHandlerDelegate(self.engine, self)

    def on_before_register(self):
        self.handler_delegate.engine_ref = self.engine

    @abstractmethod
    def on_setup_app(self, app: FastAPI, ui: gradio.blocks.Block, parent_block: Optional[gradio.blocks.Block]=None):
        pass

    @abstractmethod
    def on_setup_session_delegate(self, session_context: SessionContext, handler_context: HandlerContext,
                                  session_delegate: ClientSessionDelegate):
        pass
