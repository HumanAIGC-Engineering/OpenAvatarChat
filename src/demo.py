import inspect
import multiprocessing
import queue
import sys
from typing import Optional, Dict
from typing import Union

from utils.directory_info import DirectoryInfo
project_dir = DirectoryInfo.get_project_dir()
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from chat_engine.data_models.runtime_data.data_bundle import DataBundle
from service.logger_config_data import LoggerConfigData
from service.service_config_data import ServiceConfigData, TwilioConfigData

import argparse
import asyncio
import os
import uuid

import numpy as np
import gradio as gr
from dynaconf import Dynaconf
from gradio_webrtc.webrtc import AsyncAudioVideoStreamHandler, AudioEmitType, WebRTC
from loguru import logger

from chat_engine.chat_engine import ChatEngine
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, EngineChannelType
from chat_engine.data_models.session_info_data import SessionInfoData

from src.utils.interval_counter import IntervalCounter


chat_engine = ChatEngine()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="service host address")
    parser.add_argument("--port", type=int, help="service host port")
    parser.add_argument("--config", type=str, default="config/sample.yaml", help="config file to use")
    parser.add_argument("--env", type=str, default="default", help="environment to use in config file")
    return parser.parse_args()


def load_configs(in_args):
    os.environ["ENV_FOR_DYNACONF"] = in_args.env
    base_dir = DirectoryInfo.get_project_dir()
    if os.path.isabs(in_args.config):
        config_path = in_args.config
    else:
        config_path = os.path.join(base_dir, in_args.config)

    logger.info(f"Load config with env {in_args.env} from {config_path}")
    config = Dynaconf(
        settings_files=[config_path],
        environments=True
    )

    out_logger_config = LoggerConfigData.model_validate(config.get("logger", {}))
    out_service_config = ServiceConfigData.model_validate(config.get("service", {}))
    out_engine_config = ChatEngineConfigModel.model_validate(config.get("chat_engine", {}))
    return out_logger_config, out_service_config, out_engine_config


def config_logger(in_logger_config: LoggerConfigData):
    logger.info(f"Set log level to {in_logger_config.log_level}")
    logger.remove()
    logger.add(sys.stdout, level=in_logger_config.log_level)


def register_handlers(engine: ChatEngine):
    from chat_engine.output_handlers.output_handler_s2v import HandlerTts2Face
    engine.register_handler(HandlerTts2Face())
    from chat_engine.input_handlers.input_handler_vad import HandlerAudioVAD
    engine.register_handler(HandlerAudioVAD())
    from chat_engine.think_handlers.handler_s2s import HandlerS2SMiniCPM
    engine.register_handler(HandlerS2SMiniCPM())


def create_ssl_context(in_args, in_service_config: ServiceConfigData):
    out_ssl_context = {}
    if in_args.host:
        in_service_config.host = in_args.host
    if in_args.port:
        in_service_config.port = in_args.port

    ssl_cert_path = None
    ssl_key_path = None
    base_dir = DirectoryInfo.get_project_dir()
    if in_service_config.cert_file:
        ssl_cert_path = os.path.join(base_dir, in_service_config.cert_file) \
            if not os.path.isabs(in_service_config.cert_file) else in_service_config.cert_file
    if in_service_config.cert_key:
        ssl_key_path = os.path.join(base_dir, in_service_config.cert_key) \
            if not os.path.isabs(in_service_config.cert_key) else in_service_config.cert_key
    if ssl_cert_path and not os.path.isfile(ssl_cert_path):
        logger.warning(f"Cert file {ssl_cert_path} not found")
        ssl_cert_path = None
    if ssl_key_path and not os.path.isfile(ssl_key_path):
        logger.warning(f"Key file {ssl_key_path} not found")
        ssl_key_path = None

    logger.info(f"Service will be started on {in_service_config.host}:{in_service_config.port}")
    if ssl_cert_path and ssl_key_path:
        out_ssl_context["ssl_certfile"] = ssl_cert_path
        out_ssl_context["ssl_keyfile"] = ssl_key_path
        if os.environ["ENV_FOR_DYNACONF"] != "production":
            out_ssl_context["ssl_verify"] = False
        logger.info(f"SSL enabled.")
    return out_ssl_context


# noinspection PyUnresolvedReferences
def connect_to_twilio(config: TwilioConfigData):
    # noinspection PyPackageRequirements
    from twilio.rest import Client
    client = Client(
        config.twilio_account_sid,
        config.twilio_auth_token
    )
    token = client.tokens.create()
    out_rtc_configuration = {
        "iceServers": token.ice_servers,
        "iceTransportPolicy": "relay",
    }
    return out_rtc_configuration, (client, token)


def prepare_rtc_configuration(config: ServiceConfigData):
    client_entities = None
    out_rtc_configuration = None
    if config.rtc_config is not None:
        logger.info(f"Using RTC config: {config.rtc_config}")
        if isinstance(config.rtc_config, TwilioConfigData):
            out_rtc_configuration, client_entities = connect_to_twilio(config.rtc_config)
    return out_rtc_configuration, client_entities


class ChatStreamHandler(AsyncAudioVideoStreamHandler):
    def __init__(self, expected_layout="mono",
                 output_sample_rate=24000,
                 output_frame_size=480) -> None:
        super().__init__(
            expected_layout=expected_layout,
            output_sample_rate=output_sample_rate,
            output_frame_size=output_frame_size,
            input_sample_rate=16000,
        )

        self.audio_input_queue = asyncio.Queue()
        self.audio_output_queue = asyncio.Queue()
        self.video_output_queue = asyncio.Queue()

        self.quit = asyncio.Event()
        self.session = None
        self.last_frame_time = 0
        
        self.emit_counter = IntervalCounter("emit counter")

    def copy(self):
        return ChatStreamHandler(
            expected_layout=self.expected_layout,
            output_sample_rate=self.output_sample_rate,
            output_frame_size=self.output_frame_size,
        )

    def start_session(self):
        inputs = {
            EngineChannelType.AUDIO: self.audio_input_queue,
        }
        outputs = {
            EngineChannelType.AUDIO: self.audio_output_queue,
            EngineChannelType.VIDEO: self.video_output_queue,
        }

        session_info = SessionInfoData(
            session_id=str(uuid.uuid4()),
        )

        self.session = chat_engine.create_session(session_info=session_info,
                                                  input_queues=inputs,
                                                  output_queues=outputs)
        self.session.start()

    async def video_emit(self):
        self.emit_counter.add_property("emit_video")
        video_frame = await self._get_data_from_queue(self.video_output_queue)
        return video_frame

    async def video_receive(self, frame):
        # TODO implement video input
        pass

    async def receive(self, frame: tuple[int, np.ndarray]):
        sr, array = frame
        if self.session:
            self.audio_input_queue.put_nowait((sr, array))

    async def emit(self) -> AudioEmitType:
        try:
            if not self.args_set.is_set():
                await self.wait_for_args()
            if self.session is None:
                self.start_session()
            output = await self._get_data_from_queue(self.audio_output_queue)
            if isinstance(output, DataBundle):
                array = output.get_data("avatar_audio")
            else:
                array = output
            sample_num = array.shape[-1]
            self.emit_counter.add_property("emit_audio", sample_num / self.output_sample_rate)
        except Exception as e:
            logger.opt(exception=e).error(f"Error in emit: ")
            array = np.zeros((1, 1), dtype=np.float32)
        return self.output_sample_rate, array

    def shutdown(self):
        self.quit.set()
        if self.session is not None:
            self.session.stop()
            self.session = None
        self.quit.clear()
        
    @staticmethod
    async def _get_data_from_queue(queue: Union[asyncio.Queue, queue.Queue, multiprocessing.Queue]):
        if inspect.iscoroutinefunction(queue.get):
            return await queue.get()
        else:
            while True:
                try:
                    data = queue.get_nowait()
                    return data
                except Exception:
                    await asyncio.sleep(0.1)
                    continue


def setup_demo(_config: ServiceConfigData, in_rtc_configuration: Optional[Dict] = None):
    css = """
    footer {
        display: none !important;
    }
    """
    with gr.Blocks(css=css) as gradio_block:
        with gr.Column():
            with gr.Group():
                webrtc = WebRTC(
                    label="Avatar Chat",
                    modality="audio-video",
                    mode="send-receive",
                    elem_id="video-source",
                    rtc_configuration=in_rtc_configuration,
                    pulse_color="rgb(35, 157, 225)",
                    icon_button_color="rgb(35, 157, 225)",
                    show_local_video="picture-in-picture",
                )
            # noinspection PyTypeChecker
            webrtc.stream(
                ChatStreamHandler(),
                inputs=[webrtc],
                outputs=[webrtc],
                time_limit=900,
                concurrency_limit=1,
            )
    return gradio_block


if __name__ == "__main__":
    args = parse_args()
    logger_config, service_config, engine_config = load_configs(args)

    config_logger(logger_config)
    register_handlers(chat_engine)
    chat_engine.initialize(engine_config)
    ssl_context = create_ssl_context(args, service_config)
    rtc_configuration, rtc_entities = prepare_rtc_configuration(service_config)
    demo = setup_demo(service_config, rtc_configuration)
    demo.launch(
        server_name=service_config.host,
        server_port=service_config.port,
        **ssl_context
    )
