from functools import wraps
import time

from loguru import logger


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"Function {func.__name__} took {execution_time:.3f}s to execute.")
        return result
    return wrapper
