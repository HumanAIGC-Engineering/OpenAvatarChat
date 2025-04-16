import os

from dynaconf import Dynaconf
from loguru import logger

from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel
from engine_utils.directory_info import DirectoryInfo
from service.service_data_models.logger_config_data import LoggerConfigData
from service.service_data_models.service_config_data import ServiceConfigData


def load_configs(in_args):
    os.environ["ENV_FOR_DYNACONF"] = in_args.env
    base_dir = DirectoryInfo.get_project_dir()
    if os.path.isabs(in_args.config):
        config_path = in_args.config
    else:
        config_path = os.path.join(base_dir, in_args.config)
    if not os.path.isfile(config_path):
        logger.error(f"Config file {config_path} not found!")
        exit(1)

    logger.info(f"Load config with env {in_args.env} from {config_path}")
    config = Dynaconf(
        settings_files=[config_path],
        environments=True,
        load_dotenv=True
    )

    out_logger_config = LoggerConfigData.model_validate(config.get("logger", {}))
    out_service_config = ServiceConfigData.model_validate(config.get("service", {}))
    out_engine_config = ChatEngineConfigModel.model_validate(config.get("chat_engine", {}))
    return out_logger_config, out_service_config, out_engine_config

