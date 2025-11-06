from collections import Counter
from typing import Dict, List


from utils.bank_processing import process_bank_operations, process_bank_search

# Тесты для process_bank_search


def test_process_bank_search_found():
    """Тест: находит транзакции по точному совпадению слова в description"""
    data = [
        {"description": "Покупка в магазине Пятерочка"},
        {"description": "Оплата интернета"},
        {"description": "Перевод другу"},
    ]
    result = process_bank_search(data, "пятерочка")
    assert len(result) == 1
    assert result[0]["description"] == "Покупка в магазине Пятерочка"


def test_process_bank_search_case_insensitive():
    """Тест: поиск без учёта регистра"""
    data = [
        {"description": "Покупка в МАГНИТ"},
        {"description": "оплата ЖКХ"},
    ]
    result = process_bank_search(data, "магнит")
    assert len(result) == 1
    assert "МАГНИТ" in result[0]["description"]


def test_process_bank_search_substring():
    """Тест: поиск по подстроке"""
    data = [
        {"description": "Супермаркет Перекресток"},
        {"description": "Кафе КофеВокруг"},
    ]
    result = process_bank_search(data, "крест")
    assert len(result) == 1
    assert "Перекресток" in result[0]["description"]


def test_process_bank_search_no_match():
    """Тест: нет совпадений — возвращается пустой список"""
    data = [
        {"description": "Перевод зарплаты"},
        {"description": "Оплата телефона"},
    ]
    result = process_bank_search(data, "авиатickets")
    assert result == []


def test_process_bank_search_empty_data():
    """Тест: пустой входной список"""
    result = process_bank_search([], "поиск")
    assert result == []


def test_process_bank_search_missing_description():
    """Тест: транзакция без поля description — пропускается без ошибки"""
    data = [
        {"id": 1},  # нет description
        {"description": "Оплата такси"},
    ]
    result = process_bank_search(data, "такси")
    assert len(result) == 1
    assert "такси" in result[0]["description"].lower()


def test_process_bank_search_special_chars():
    """Тест: поиск со спецсимволами (экранирование работает)"""
    data = [
        {"description": "Оплата за услугу VIP-доступ!"},
        {"description": "Скидка 50% на всё"},
    ]
    result = process_bank_search(data, "VIP-доступ!")
    assert len(result) == 1
    assert "VIP-доступ!" in result[0]["description"]

    result2 = process_bank_search(data, "50%")
    assert len(result2) == 1
    assert "50%" in result2[0]["description"]


def test_process_bank_search_empty_search():
    """Тест: пустая строка для поиска — находит все транзакции с description"""
    data = [
        {"description": "Покупка"},
        {"description": ""},
        {"id": 1},  # без description
    ]
    result = process_bank_search(data, "")
    # Находят только записи с непустым description
    assert len(result) == 3
    assert result[0]["description"] == "Покупка"


# Тесты для process_bank_operations


def test_process_bank_operations_simple():
    """Тест: простой подсчёт категорий"""
    data = [
        {"description": "Покупка в магазине Пятерочка"},
        {"description": "Оплата интернета от Ростелеком"},
        {"description": "Перевод другу на карту"},
    ]
    categories = ["Пятерочка", "Ростелеком", "Перевод"]
    result = process_bank_operations(data, categories)
    assert result == {"Пятерочка": 1, "Ростелеком": 1, "Перевод": 1}


def test_process_bank_operations_case_insensitive():
    """Тест: поиск категорий без учёта регистра"""
    data = [
        {"description": "оплата за интернет от РОСТЕЛЕКОМ"},
        {"description": "покупка в магазине ПЯТЕРОЧКА"},
    ]
    categories = ["Ростелеком", "Пятерочка"]
    result = process_bank_operations(data, categories)
    assert result == {"Ростелеком": 1, "Пятерочка": 1}


def test_process_bank_operations_no_matches():
    """Тест: категории не найдены — возвращается пустой словарь"""
    data = [
        {"description": "Зарплата"},
        {"description": "Коммунальные платежи"},
    ]
    categories = ["Авиабилеты", "Отель"]
    result = process_bank_operations(data, categories)
    assert result == {}


def test_process_bank_operations_partial_match():
    """Тест: частичное совпадение категории в описании"""
    data = [
        {"description": "Супермаркет Перекресток на Ленина"},
        {"description": "Кафе Перекресток вкуса"},
    ]
    categories = ["Перекресток"]
    result = process_bank_operations(data, categories)
    assert result == {"Перекресток": 2}


def test_process_bank_operations_empty_data():
    """Тест: пустой список транзакций"""
    result = process_bank_operations([], ["Пятерочка", "Ростелеком"])
    assert result == {}


def test_process_bank_operations_empty_categories():
    """Тест: пустой список категорий"""
    data = [{"description": "Покупка в Пятерочке"}]
    result = process_bank_operations(data, [])
    assert result == {}


def test_process_bank_operations_duplicate_categories():
    """Тест: повторяющиеся категории в списке — учитываются один раз"""
    data = [
        {"description": "Покупка в Пятерочке"},
        {"description": "Перевод другу"},
    ]
    categories = ["Пятерочка", "Пятерочка", "Перевод"]
    result = process_bank_operations(data, categories)
    # Категория "Пятерочка" учтена один раз, но найдена 1 транзакция
    assert result == {"Перевод": 1}


def test_process_bank_operations_overlap():
    """Тест: одна транзакция подходит под несколько категорий"""
    data = [
        {"description": "Покупка продуктов в Магните и Пятерочке"},
    ]
    categories = ["Магнит", "Пятерочка"]
    result = process_bank_operations(data, categories)
    assert result == {"Магнит": 1}
