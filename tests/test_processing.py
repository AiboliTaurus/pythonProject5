import pytest


from src.processing import filter_by_state, sort_by_date


# Тесты для filter_by_state
def test_filter_by_state_default():
    # Базовый тест с состоянием по умолчанию (EXECUTED)
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-02-01"},
        {"id": 3, "state": "EXECUTED", "date": "2023-03-01"},
    ]

    result = filter_by_state(operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_custom():
    # Тест с пользовательским состоянием
    operations = [
        {"id": 1, "state": "PENDING", "date": "2023-01-01"},
        {"id": 2, "state": "PENDING", "date": "2023-02-01"},
        {"id": 3, "state": "EXECUTED", "date": "2023-03-01"},
    ]

    result = filter_by_state(operations, "PENDING")
    assert len(result) == 2
    assert all(op["state"] == "PENDING" for op in result)


def test_filter_by_state_no_matches():
    # Тест когда нет подходящих операций
    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "CANCELED", "date": "2023-02-01"},
    ]

    result = filter_by_state(operations, "PENDING")
    assert len(result) == 0


def test_filter_by_state_invalid_input():
    # Тест с некорректным входным параметром (не список) — должно вызвать ошибку
    with pytest.raises(ValueError, match="Первый аргумент должен быть списком операций"):
        filter_by_state("не_список")

    # Тест с элементом, который не является словарём — теперь не вызывает ошибку, а фильтрует
    result = filter_by_state([123, "строка", {"state": "EXECUTED"}])
    assert result == [{"state": "EXECUTED"}]  # только валидный словарь попал в результат

    # Тест с отсутствием ключа 'state' в словаре — теперь не вызывает ошибку, а фильтрует
    result = filter_by_state([{"id": 1, "amount": 100}, {"state": "EXECUTED"}])
    assert result == [{"state": "EXECUTED"}]  # только запись с 'state' попала в результат

    # Тест с корректным state (строка) — не должно вызывать ошибку
    filter_by_state([{"state": "EXECUTED"}], state="123")

    # Тест с пустым списком (валидный случай)
    assert filter_by_state([]) == []

    # Тест с None в списке — теперь не вызывает ошибку, а фильтрует
    result = filter_by_state([None, {"state": "EXECUTED"}])
    assert result == [{"state": "EXECUTED"}]  # None отфильтрован

    # Тест с некорректным типом state (число вместо строки) — должно вызвать ошибку
    with pytest.raises(ValueError, match="Параметр state должен быть строкой"):
        filter_by_state([{"state": "EXECUTED"}], state=123)

    # Тест с корректным state (по умолчанию)
    filter_by_state([{"state": "EXECUTED"}])


# Тесты для sort_by_date
def test_sort_by_date_descending():
    # Тест сортировки по убыванию
    operations = [
        {"id": 1, "date": "2023-01-01T00:00:00"},
        {"id": 2, "date": "2023-03-01T00:00:00"},
        {"id": 3, "date": "2023-02-01T00:00:00"},
    ]

    result = sort_by_date(operations)
    expected_dates = ["2023-03-01T00:00:00", "2023-02-01T00:00:00", "2023-01-01T00:00:00"]
    assert [op["date"] for op in result] == expected_dates


def test_sort_by_date_ascending():
    # Тест сортировки по возрастанию
    operations = [
        {"id": 1, "date": "2023-03-01T00:00:00"},
        {"id": 2, "date": "2023-01-01T00:00:00"},
        {"id": 3, "date": "2023-02-01T00:00:00"},
    ]
    assert '[op["date"]]'
