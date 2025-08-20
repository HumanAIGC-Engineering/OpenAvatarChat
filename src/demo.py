import sys

import gradio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from engine_utils.directory_info import DirectoryInfo
from service.service_utils.logger_utils import config_loggers
from service.service_utils.service_config_loader import load_configs
from service.service_utils.ssl_helpers import create_ssl_context

project_dir = DirectoryInfo.get_project_dir()
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)


import argparse
import os

import gradio as gr

from chat_engine.chat_engine import ChatEngine


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="service host address")
    parser.add_argument("--port", type=int, help="service host port")
    parser.add_argument("--config", type=str, default="config/chat_with_openai_compatible_bailian_cosyvoice.yaml", help="config file to use")
    parser.add_argument("--env", type=str, default="default", help="environment to use in config file")
    return parser.parse_args()


class OpenAvatarChatWebServer(uvicorn.Server):

    def __init__(self, chat_engine: ChatEngine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_engine = chat_engine
    
    async def shutdown(self, sockets=None):
        logger.info("Start normal shutdown process")
        self.chat_engine.shutdown()
        await super().shutdown(sockets)


def setup_demo():
    app = FastAPI()

    @app.get("/")
    def get_root():
        return RedirectResponse(url="/ui")

    @app.get("/ui/static/fonts/system-ui/system-ui-Regular.woff2")
    @app.get("/ui/static/fonts/ui-sans-serif/ui-sans-serif-Regular.woff2")
    @app.get("/favicon.ico")
    def get_font():
        # remove confusing error
        return {}

    css = """


    .app {
        @media screen and (max-width: 768px) {
            padding: 8px !important;
        }
    }
    footer {
        display: none !important;
    }
    """
    with gr.Blocks(css=css) as gradio_block:
        with gr.Column():
            with gr.Group() as rtc_container:
                pass
    gradio.mount_gradio_app(app, gradio_block, "/ui")
    return app, gradio_block, rtc_container

def main():
    args = parse_args()
    logger_config, service_config, engine_config = load_configs(args)


    # 设置modelscope的默认下载地址
    if not os.path.isabs(engine_config.model_root):
        os.environ['MODELSCOPE_CACHE'] = os.path.join(DirectoryInfo.get_project_dir(),
                                                      engine_config.model_root.replace('models', ''))

    config_loggers(logger_config)
    chat_engine = ChatEngine()
    demo_app, ui, parent_block = setup_demo()

    chat_engine.initialize(engine_config, app=demo_app, ui=ui, parent_block=parent_block)

    ssl_context = create_ssl_context(args, service_config)

    uvicorn_config = uvicorn.Config(demo_app, host=service_config.host, port=service_config.port, **ssl_context)
    server = OpenAvatarChatWebServer(chat_engine, uvicorn_config)
    server.run()

    # uvicorn.run(demo_app, host=service_config.host, port=service_config.port, **ssl_context)


if __name__ == "__main__":
    main()