import csv
from typing import List, Dict


def load_csv(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из CSV-файла

    Args:
        file_path (str): путь к CSV-файлу

    Returns:
        List[Dict]: список словарей с транзакциями
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении CSV: {str(e)}")
