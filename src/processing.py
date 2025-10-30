def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """
    Фильтрует список операций по указанному состоянию

    Args:
        operations (list): список словарей с данными операций
        state (str): значение состояния для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        list: отфильтрованный список операций

    Raises:
        ValueError: если входные данные некорректны
    """
    # Проверяем, что operations является списком
    if not isinstance(operations, list):
        raise ValueError("Первый аргумент должен быть списком операций")

    # Проверяем, что все элементы списка являются словарями
    for operation in operations:
        if not isinstance(operation, dict):
            raise ValueError("Все элементы списка должны быть словарями")

        # Проверяем наличие ключа 'state' в каждом словаре
        if "state" not in operation:
            raise ValueError("Каждый словарь должен содержать ключ 'state'")

    # Проверяем, что state является строкой
    if not isinstance(state, str):
        raise ValueError("Параметр state должен быть строкой")

    # Фильтруем операции по состоянию
    filtered_operations = [operation for operation in operations if operation.get("state") == state]

    return filtered_operations


from datetime import datetime


def sort_by_date(operations: list, descending: bool = True) -> list:
    """
    Сортирует список операций по дате

    Args:
        operations (list): список словарей с операциями
        descending (bool): порядок сортировки (True - убывание, False - возрастание)

    Returns:
        list: отсортированный список операций
    """
    # Проверяем, что входные данные корректны
    if not isinstance(operations, list):
        raise ValueError("Первый аргумент должен быть списком операций")

    # Функция для извлечения даты из словаря
    def get_date(operation):
        try:
            # Преобразуем строку в объект datetime
            return datetime.fromisoformat(operation["date"])
        except (KeyError, ValueError):
            # Если дата отсутствует или некорректна, возвращаем минимальную дату
            return datetime.min

    # Сортируем операции по дате
    sorted_operations = sorted(operations, key=get_date, reverse=descending)

    return sorted_operations
