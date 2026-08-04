import runpy
import sys
import types
from pathlib import Path


class RecordingLogger:
    def __init__(self):
        self.exception_messages = []

    def exception(self, message):
        self.exception_messages.append(message)

    def info(self, _message):
        pass


def install_module(monkeypatch, name, **attributes):
    module = types.ModuleType(name)
    for attribute, value in attributes.items():
        setattr(module, attribute, value)
    monkeypatch.setitem(sys.modules, name, module)
    return module


def load_demo(monkeypatch):
    class FakeChatEngine:
        pass

    class FakeServer:
        pass

    class FakeFastAPI:
        pass

    class FakeDirectoryInfo:
        @staticmethod
        def get_project_dir():
            return "/tmp/open-avatar-chat"

    logger = RecordingLogger()

    install_module(monkeypatch, "chat_engine")
    install_module(monkeypatch, "chat_engine.chat_engine", ChatEngine=FakeChatEngine)
    install_module(monkeypatch, "gradio")
    install_module(monkeypatch, "uvicorn", Server=FakeServer, Config=object)
    install_module(monkeypatch, "fastapi", FastAPI=FakeFastAPI)
    install_module(monkeypatch, "loguru", logger=logger)
    install_module(monkeypatch, "engine_utils")
    install_module(monkeypatch, "engine_utils.directory_info", DirectoryInfo=FakeDirectoryInfo)
    install_module(monkeypatch, "service")
    install_module(monkeypatch, "service.service_utils")
    install_module(monkeypatch, "service.service_utils.logger_utils", config_loggers=lambda *_args: None)
    install_module(monkeypatch, "service.service_utils.service_config_loader", load_configs=lambda *_args: None)
    install_module(monkeypatch, "service.service_utils.ssl_helpers", create_ssl_context=lambda *_args: None)
    install_module(monkeypatch, "torch", load=lambda *_args, **_kwargs: None)

    demo_path = Path(__file__).parents[1] / "src" / "demo.py"
    namespace = runpy.run_path(demo_path, run_name="demo_under_test")
    return namespace, logger


def test_run_main_logs_unhandled_startup_failure_and_returns_nonzero(monkeypatch):
    namespace, logger = load_demo(monkeypatch)
    run_main = namespace.get("_run_main")

    assert callable(run_main), "demo.py must expose a testable entrypoint wrapper"

    def fail_startup():
        raise RuntimeError("startup failed")

    run_main.__globals__["main"] = fail_startup

    assert run_main() == 1
    assert logger.exception_messages == ["OpenAvatarChat failed to start"]
