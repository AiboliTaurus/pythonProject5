import functools
import logging
from typing import Any, Callable


def log(filename: str = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    :param filename: имя файла для записи логов (None для вывода в консоль)
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger = logging.getLogger(func.__name__)

            # Настройка логгера
            if filename:
                handler = logging.FileHandler(filename)
            else:
                handler = logging.StreamHandler()

            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result
            except Exception as e:
                logger.info(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise
            finally:
                logger.removeHandler(handler)

        return wrapper

    return decorator
