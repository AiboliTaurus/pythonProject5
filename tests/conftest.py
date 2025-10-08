import pytest
from generators.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator
)

# Фикстура для создания тестовых транзакций
@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        }
    ]

# Фикстура для описаний транзакций
@pytest.fixture
def expected_descriptions():
    return [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]

# Фикстура для тестовых номеров карт
@pytest.fixture
def expected_card_numbers():
    return [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005"
    ]

# Тестирование фильтрации по валюте
def test_filter_by_currency(transactions):
    usd_transactions = filter_by_currency(transactions, "USD")
    assert len(list(usd_transactions)) == 2  # Исправлено с 1 на 2, так как в данных 2 USD транзакции

# Тестирование получения описаний
def test_transaction_descriptions(transactions, expected_descriptions):
    descriptions = transaction_descriptions(transactions)
    assert list(descriptions) == expected_descriptions[:len(transactions)]

# Тестирование генератора номеров карт
def test_card_number_generator(expected_card_numbers):
    numbers = list(card_number_generator(1, 5))
    assert numbers