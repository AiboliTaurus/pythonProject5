import re
from collections import Counter
from typing import List, Dict


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Функция поиска транзакций по строке в описании с использованием регулярных выражений

    Args:
        data (List[Dict]): Список словарей с данными о транзакциях
        search (str): Строка для поиска в описании транзакций

    Returns:
        List[Dict]: Отфильтрованный список словарей с найденными транзакциями
    """
    # Создаем регулярное выражение с учетом регистра и экранированием спецсимволов
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    # Фильтруем транзакции, используя регулярное выражение
    return [transaction for transaction in data if pattern.search(transaction.get("description", ""))]


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict:
    """
    Функция подсчета количества операций по категориям

    Args:
        data (List[Dict]): Список словарей с данными о транзакциях
        categories (List[str]): Список категорий для подсчета

    Returns:
        Dict: Словарь с количеством операций по каждой категории
    """
    # Создаем счетчик
    category_counts = Counter()

    # Проходим по каждой транзакции
    for transaction in data:
        # Получаем описание операции в нижнем регистре
        description = transaction.get("description", "").lower()

        # Проверяем наличие каждой категории в описании
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    return dict(category_counts)
