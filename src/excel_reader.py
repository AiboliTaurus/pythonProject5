from typing import Dict, List

import pandas as pd


def load_excel(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из Excel-файла

    Args:
        file_path (str): путь к Excel-файлу

    Returns:
        List[Dict]: список словарей с транзакциями
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel: {str(e)}")
