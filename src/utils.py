# src/utils.py
import json
import os
from typing import Any


def load_transactions(file_path: str) -> Any:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        Any: Данные из файла или пустой список при ошибках
    """
    # Проверка существования файла
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Проверка, что данные — список
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, IOError):
        return []
