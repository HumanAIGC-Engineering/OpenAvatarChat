import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from engine_utils.directory_info import DirectoryInfo
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel
from service.manager_service.data_tool_service import ManagerDataToolService

_data_tool_service: Optional[ManagerDataToolService] = None
_data_tool_base_dir: Optional[Path] = None


def get_data_tool_base_dir() -> Path:
    """
    Base directory for data tool dumped files: <project>/temp/data_tool
    """
    global _data_tool_base_dir
    if _data_tool_base_dir is None:
        project_dir = Path(DirectoryInfo.get_project_dir())
        _data_tool_base_dir = project_dir / "temp" / "data_tool"
    return _data_tool_base_dir


def ensure_data_tool_service(buffer_limit: int = 200) -> ManagerDataToolService:
    """
    Ensure there is a singleton data tool service and update its buffer limit.
    Called by handlers during load.
    """
    global _data_tool_service
    if _data_tool_service is None:
        _data_tool_service = ManagerDataToolService(buffer_limit=buffer_limit)
    else:
        _data_tool_service.update_buffer_limit(buffer_limit)
    return _data_tool_service


def register_data_tool_service(service: ManagerDataToolService):
    """
    Explicitly register a data tool service instance.
    """
    global _data_tool_service
    _data_tool_service = service
    return _data_tool_service


def get_data_tool_service() -> Optional[ManagerDataToolService]:
    return _data_tool_service


def register_manager_apis(app: FastAPI, engine_config: Optional[ChatEngineConfigModel] = None):
    """
    Register manager APIs (data tool service).
    """
    data_tool_service = get_data_tool_service()
    if data_tool_service is not None:
        data_tool_service.register_routes(app)
        logger.info("Manager data tool websocket registered.")

    @app.get("/download/manager/data_tool/file")
    async def get_data_tool_file(file_path: str):
        """
        Serve files stored by the data tool handler. The file_path must be a
        relative path under the data_tool base directory.
        """
        base_dir = get_data_tool_base_dir()
        target_path = (base_dir / file_path).resolve()

        try:
            base_dir_resolved = base_dir.resolve()
        except FileNotFoundError:
            base_dir.mkdir(parents=True, exist_ok=True)
            base_dir_resolved = base_dir.resolve()

        if base_dir_resolved not in target_path.parents and target_path != base_dir_resolved:
            raise HTTPException(status_code=400, detail="Invalid file path.")
        if not target_path.exists() or not target_path.is_file():
            raise HTTPException(status_code=404, detail="File not found.")

        return FileResponse(target_path)

    logger.info("Manager service APIs registered.")
