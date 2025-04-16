import os

from loguru import logger

from engine_utils.directory_info import DirectoryInfo
from service.service_data_models.service_config_data import ServiceConfigData


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
        logger.info(f"SSL enabled.")
    return out_ssl_context
