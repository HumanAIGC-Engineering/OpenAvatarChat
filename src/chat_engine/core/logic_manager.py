import inspect
import os
import sys
import time
import weakref
from dataclasses import dataclass, field
from types import ModuleType
from typing import Optional, Dict, Tuple

from loguru import logger

from engine_utils.import_utils import import_class
from engine_utils.path_utils import validate_search_path

from chat_engine.common.logic_base import LogicBase

from chat_engine.data_models.internal.logic_definition_data import LogicBaseInfo

from chat_engine.data_models.chat_engine_config_data import LogicBaseConfigModel, ChatEngineConfigModel


@dataclass
class LogicRegistry:
    base_info: Optional[LogicBaseInfo] = field(default=None)
    logic: Optional[LogicBase] = field(default=None)
    logic_config: Optional[LogicBaseConfigModel] = field(default=None)


class LogicManager:
    def __init__(self, engine):
        # [logic_module_name, (module, logic_class)]
        self.logic_modules: Dict[str, Tuple[ModuleType, type[LogicBase]]] = {}
        # [logic_name, logic_registry]
        self.logic_registries: Dict[str, LogicRegistry] = {}
        # [logic_name, logic_config]
        self.logic_configs: Dict[str, Dict] = {}
        self.search_path = []

        self.engine_ref = weakref.ref(engine)

    def add_search_path(self, path: str):
        path = validate_search_path(path)
        if path is None:
            logger.warning(f"Path {path} is not a directory, it is not added to search path.")
            return
        if path not in self.search_path:
            self.search_path.append(path)
            if path not in sys.path:
                sys.path.append(path)

    def initialize(self, engine_config: ChatEngineConfigModel):
        if engine_config.logic_search_path:
            for search_path in engine_config.logic_search_path:
                self.add_search_path(search_path)
        if engine_config.logic_configs:
            for logic_name, logic_config in engine_config.logic_configs.items():
                self.logic_configs[logic_name] = logic_config
        logger.info(f"Use logic search path: {self.search_path}")
        for logic_name, raw_config in self.logic_configs.items():
            try:
                logic_config = LogicBaseConfigModel.model_validate(raw_config)
            except Exception as e:
                logger.error(f"Failed to parse logic config for {logic_name}: {e}")
                continue
            if not logic_config.enabled:
                continue
            if logic_config.module is None:
                logger.warning(f"Logic {logic_name} has no module specified, skipping.")
                continue
            module, logic_class = import_class(logic_config.module, LogicBase, self.search_path)
            self.logic_modules[logic_config.module] = module, logic_class
            self.register_logic(logic_name, logic_class())

    def register_logic(self, name: str, logic: LogicBase):
        registry = self.logic_registries.setdefault(name, LogicRegistry())
        logic_module = inspect.getmodule(type(logic))
        logic_root = os.path.split(logic_module.__file__)[0]
        logic.logic_root = logic_root
        logic.engine = self.engine_ref
        if registry.base_info is None:
            logic.on_before_register()
            base_info = logic.get_logic_info()
            base_info.name = name
            raw_config = self.logic_configs.get(name, {})
            if not issubclass(base_info.config_model, LogicBaseConfigModel):
                raise ValueError(f"Logic {name} provides invalid config model {base_info.config_model}")
            config: LogicBaseConfigModel = base_info.config_model.model_validate(raw_config)
            registry.logic_config = config
            registry.base_info = base_info
            registry.logic = logic
            logger.info(f"Registered logic {name}({type(logic)}) with config: {config}")

    def get_enabled_logics(self, order_by_priority=True):
        result = []
        for logic_name, registry in self.logic_registries.items():
            if registry.logic is None or registry.logic_config is None:
                continue
            if not registry.logic_config.enabled:
                continue
            result.append(registry)
        if order_by_priority:
            result.sort(key=lambda x: x.base_info.load_priority)
        return result

    def load_logics(self, engine_config: ChatEngineConfigModel):
        enabled_logics = self.get_enabled_logics()
        for logic_registry in enabled_logics:
            load_start = time.monotonic()
            logic_registry.logic.load(engine_config, logic_registry.logic_config)
            dur_load = time.monotonic() - load_start
            logger.info(f"Logic {logic_registry.base_info.name} loaded in {round(dur_load * 1e3)} milliseconds")

    def destroy(self):
        for logic_name, registry in self.logic_registries.items():
            if registry.logic is None or registry.logic_config is None:
                continue
            if not registry.logic_config.enabled:
                continue
            logger.info(f"Destroying logic {logic_name}")
            registry.logic.destroy()
            logger.info(f"Logic {logic_name} destroyed")
