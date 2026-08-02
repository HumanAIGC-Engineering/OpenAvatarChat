import importlib
import sys
import types
from enum import Enum
from pathlib import Path

import yaml
from pydantic import BaseModel


def install_module(name: str, **attrs):
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module
    return module


class _Logger:
    def __getattr__(self, _name):
        return lambda *args, **kwargs: None


class _HandlerBase:
    def __init__(self):
        pass


class _HandlerBaseConfigModel(BaseModel):
    pass


class _HandlerContext:
    def __init__(self, session_id: str):
        self.session_id = session_id


class _HandlerBaseInfo(dict):
    pass


class _HandlerDataInfo(dict):
    pass


class _HandlerDetail(dict):
    pass


class _ChatDataType(Enum):
    HUMAN_TEXT = "human_text"
    CAMERA_VIDEO = "camera_video"
    AVATAR_TEXT = "avatar_text"


class _OpenAI:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class _APIStatusError(Exception):
    body = None


def install_llm_handler_stubs():
    install_module("loguru", logger=_Logger())
    install_module("openai", APIStatusError=_APIStatusError, OpenAI=_OpenAI)
    install_module("chat_engine")
    install_module("chat_engine.contexts")
    install_module("chat_engine.contexts.handler_context", HandlerContext=_HandlerContext)
    install_module("chat_engine.contexts.session_context", SessionContext=object)
    install_module("chat_engine.common")
    install_module("chat_engine.common.handler_base",
                   HandlerBase=_HandlerBase,
                   HandlerBaseInfo=_HandlerBaseInfo,
                   HandlerDataInfo=_HandlerDataInfo,
                   HandlerDetail=_HandlerDetail)
    install_module("chat_engine.data_models")
    install_module("chat_engine.data_models.chat_engine_config_data",
                   ChatEngineConfigModel=object,
                   HandlerBaseConfigModel=_HandlerBaseConfigModel)
    install_module("chat_engine.data_models.chat_data")
    install_module("chat_engine.data_models.chat_data.chat_data_model", ChatData=object)
    install_module("chat_engine.data_models.chat_data_type", ChatDataType=_ChatDataType)
    install_module("chat_engine.data_models.chat_signal",
                   ChatSignal=object,
                   SignalFilterRule=lambda *args, **kwargs: (args, kwargs))
    install_module("chat_engine.data_models.chat_signal_type",
                   ChatSignalType=types.SimpleNamespace(STREAM_CANCEL="stream_cancel"))
    install_module("chat_engine.data_models.chat_stream", StreamKey=str)
    install_module("chat_engine.data_models.chat_stream_config",
                   ChatStreamConfig=lambda **kwargs: kwargs)
    install_module("chat_engine.data_models.runtime_data")
    install_module("chat_engine.data_models.runtime_data.data_bundle",
                   DataBundle=object,
                   DataBundleDefinition=type(
                       "DataBundleDefinition",
                       (),
                       {"add_entry": lambda self, entry: None},
                   ),
                   DataBundleEntry=types.SimpleNamespace(
                       create_text_entry=lambda name: name,
                       create_audio_entry=lambda *args: args,
                   ))
    install_module("handlers.llm.openai_compatible.chat_history_manager",
                   ChatHistory=lambda **kwargs: object(),
                   HistoryMessage=lambda **kwargs: kwargs)


def import_llm_handler():
    install_llm_handler_stubs()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    sys.modules.pop(
        "handlers.llm.openai_compatible.llm_handler_openai_compatible",
        None,
    )
    return importlib.import_module(
        "handlers.llm.openai_compatible.llm_handler_openai_compatible"
    )


def test_resolve_api_key_prefers_explicit_value(monkeypatch):
    module = import_llm_handler()
    monkeypatch.setenv("ATLASCLOUD_API_KEY", "env-key")

    config = module.LLMConfig(api_key="explicit-key", api_key_env="ATLASCLOUD_API_KEY")

    assert module.HandlerLLM.resolve_api_key(config) == "explicit-key"


def test_resolve_api_key_reads_configured_environment_variable(monkeypatch):
    module = import_llm_handler()
    monkeypatch.setenv("ATLASCLOUD_API_KEY", "env-key")

    config = module.LLMConfig(api_key_env="ATLASCLOUD_API_KEY")

    assert module.HandlerLLM.resolve_api_key(config) == "env-key"


def test_atlascloud_preset_uses_atlas_environment_variable():
    config_path = (
        Path(__file__).resolve().parents[1]
        / "config"
        / "chat_with_atlascloud_edge_tts.yaml"
    )

    config = yaml.safe_load(config_path.read_text())
    llm_config = config["default"]["chat_engine"]["handler_configs"][
        "LLMOpenAICompatible"
    ]

    assert llm_config["api_url"] == "https://api.atlascloud.ai/v1"
    assert llm_config["api_key_env"] == "ATLASCLOUD_API_KEY"
    assert llm_config["model_name"] == "qwen/qwen3.5-flash"
