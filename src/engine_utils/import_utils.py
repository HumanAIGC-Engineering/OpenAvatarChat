import importlib
import inspect
import os
from typing import List

from loguru import logger


def import_class(module_name: str, base_class: type, search_paths: List[str]):
    module_path = None
    module_import_path = None
    for search_path in search_paths:
        find_path = os.path.join(search_path, f"{module_name}.py")
        if os.path.exists(find_path):
            module_path = find_path
            module_import_path = module_name.replace("\/", ".").replace("/", ".")
            break
    if module_path is None:
        raise ValueError(f"Module {module_name} not found in search path.")
    try:
        logger.info(f"Try to load {module_import_path}")
        module = importlib.import_module(module_import_path)
    except Exception:
        logger.error(f"Failed to import module {module_name}")
        raise
    result_class = None
    for name, obj in inspect.getmembers(module):
        if not inspect.isclass(obj):
            continue
        if inspect.isabstract(obj):
            continue
        if issubclass(obj, base_class):
            result_class = obj
            break
    if result_class is None:
        raise ValueError(f"Module {module_name} does not contain a {base_class.__name__} subclass.")
    return module, result_class
