"""
Shared frontend registration utilities.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import gradio
from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from src.engine_utils.directory_info import DirectoryInfo

InitConfigSource = Union[Dict[str, Any], Callable[[], Dict[str, Any]]]


@dataclass
class FrontendRegistrationOptions:
    """
    Options that control how the shared frontend is mounted.
    """

    mount_path: str = "/ui"
    root_route: str = "/"
    redirect_target: str = "/ui/index.html"
    init_config_route: str = "/openavatarchat/initconfig"
    frontend_dist_relative_path: str = "service/frontend_service/frontend/dist"
    gradio_placeholder_html: str = (
        """
        <h1 id="openavatarchat">
           The Gradio page is no longer available. Please use the openavatarchat-webui submodule instead.
        </h1>
        """
    )


def _resolve_frontend_path(options: FrontendRegistrationOptions) -> Path:
    return Path(DirectoryInfo.get_src_dir()) / options.frontend_dist_relative_path


def _materialize_init_config(init_config: InitConfigSource) -> Dict[str, Any]:
    if callable(init_config):
        config = init_config()
    else:
        config = copy.deepcopy(init_config)

    if not isinstance(config, dict):
        raise ValueError("init_config must resolve to a dictionary.")

    return config


def register_frontend(
    app: FastAPI,
    ui: gradio.blocks.Block,
    parent_block: Optional[gradio.blocks.Block],
    init_config: InitConfigSource,
    options: Optional[FrontendRegistrationOptions] = None,
):
    """
    Register the shared Web UI, init config endpoint, and placeholder Gradio notice.
    """

    opts = options or FrontendRegistrationOptions()
    frontend_path = _resolve_frontend_path(opts)

    @app.get(opts.init_config_route)
    async def init_config_endpoint():
        config = _materialize_init_config(init_config)
        return JSONResponse(status_code=200, content=config)

    if frontend_path.exists():
        logger.info(f"Serving frontend from {frontend_path}")
        app.mount(opts.mount_path, StaticFiles(directory=frontend_path), name="static")
        app.add_route(opts.root_route, RedirectResponse(url=opts.redirect_target))
    else:
        logger.warning(f"Frontend directory {frontend_path} does not exist")
        app.add_route(opts.root_route, RedirectResponse(url="/gradio"))

    active_parent = parent_block or ui
    with ui:
        with active_parent:
            gradio.components.HTML(opts.gradio_placeholder_html, visible=True)

