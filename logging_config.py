import logging
import os
from pathlib import Path


def get_project_root() -> Path:
    """Находит корень проекта по ключевым маркерам."""
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        if (current / "pyproject.toml").exists():
            return current
        if (current / "setup.py").exists():
            return current
        current = current.parent
    return Path(__file__).parent.resolve()


PROJECT_ROOT = get_project_root()
LOG_DIR = PROJECT_ROOT / "logs"

# Проверка и создание папки logs с обработкой ошибок
try:
    os.makedirs(LOG_DIR, exist_ok=True)
    # Пробная запись для проверки прав
    with open(LOG_DIR / ".permission_test", "w") as f:
        f.write("test")
    os.remove(LOG_DIR / ".permission_test")
except (PermissionError, OSError) as e:
    raise RuntimeError(f"Нет прав на запись в {LOG_DIR}: {e}")


def setup_logger(module_name: str) -> logging.Logger:
    """
    Настраивает логер для модуля с уникальным файлом лога.
    Гарантирует отсутствие дублирующих обработчиков.
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    log_file = LOG_DIR / f"{module_name}.log"

    # Проверка на уже существующий корректный FileHandler
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            if handler.baseFilename == str(log_file):
                return logger  # Обработчик уже настроен

    # Удаление старых FileHandler'ов
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)

    # Настройка нового обработчика
    try:
        file_handler = logging.FileHandler(str(log_file), mode="w", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (PermissionError, OSError) as e:
        logger.error(f"Ошибка при настройке логгера для {module_name}: {e}")
        raise

    return logger
