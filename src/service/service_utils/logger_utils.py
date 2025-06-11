import sys

from loguru import logger
from service.service_data_models.logger_config_data import LoggerConfigData


def config_loggers(in_logger_config: LoggerConfigData):
    logger.info(f"Set log level to {in_logger_config.log_level}")
    logger.remove()
    logger.add(sys.stdout, level=in_logger_config.log_level)
    logger.add("logs/log.log", rotation="10 MB", retention=10, encoding="utf-8", enqueue=True)
