import json
import logging
import os
from typing import Any

from logging_config import setup_logger

# Настройка логера для модуля utils
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger = setup_logger("utils")


def load_transactions(file_path: str) -> Any:
    """
    Загружает транзакции из JSON-файла.
    Args:
        file_path (str): Путь к JSON-файлу
    Returns:
        Any: Данные из файла или пустой список при ошибках
    """
    if not os.path.exists(file_path):
        logger.warning("Файл %s не найден", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.info("Файл %s успешно загружен (%d записей)", file_path, len(data))
                return data
            else:
                logger.error("Файл %s содержит данные не в формате списка", file_path)
                return []
    except json.JSONDecodeError as e:
        logger.error("Ошибка декодирования JSON в файле %s: %s", file_path, str(e))
        return []
    except IOError as e:
        logger.error("Ошибка чтения файла %s: %s", file_path, str(e))
        return []
