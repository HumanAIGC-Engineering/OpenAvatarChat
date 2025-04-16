from typing import Tuple, Union
from loguru import logger
import numpy as np

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.runtime_data.data_bundle import DataBundle

HandlerResultType = Union[
    ChatData,
    DataBundle,
    Tuple[ChatDataType, np.ndarray]
]


class HandlerContext(object):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.owner = None
        self.data_submitter = None

    def submit_data(self, data: HandlerResultType):
        if self.data_submitter is None:
            logger.error("Session is not started, data submitter not ready.")
            return
        self.data_submitter.submit(data)
