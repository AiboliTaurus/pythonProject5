def filter_by_currency(transactions, currency):
    """
    Фильтрует список транзакций по указанной валюте.

    Параметры:
    transactions (list): Список транзакций.
    currency (str): Код валюты для фильтрации.

    Возвращает:
    generator: Генератор транзакций, соответствующих указанной валюте.
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions):
    """
    Извлекает описания транзакций из списка.

    Параметры:
    transactions (list): Список транзакций.

    Возвращает:
    generator: Генератор описаний транзакций. Если описание отсутствует, возвращается 'Нет описания'.
    """
    for transaction in transactions:
        yield transaction.get("description", "Нет описания")


def card_number_generator(start, end):
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Параметры:
    start (int): Начальное значение номера карты.
    end (int): Конечное значение номера карты.

    Возвращает:
    generator: Генератор номеров карт в указанном диапазоне.
    """
    for number in range(start, end + 1):
        formatted = f"{number:016d}"
        yield f"{formatted[:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:]}"
