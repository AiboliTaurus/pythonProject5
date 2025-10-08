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

# Параметризованный тест для фильтрации по валюте
@pytest.mark.parametrize(
    "currency, expected_count",
    [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0)  # Проверка отсутствия валюты
    ]
)
def test_filter_by_currency(transactions, currency, expected_count):
    filtered = filter_by_currency(transactions, currency)
    assert len(list(filtered)) == expected_count

# Параметризованный тест для описаний транзакций
@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        (
            [
                {"description": "Перевод организации"},
                {"description": "Перевод со счета на счет"},
                {"description": "Перевод с карты на карту"}
            ],
            [
                "Перевод организации",
                "Перевод со счета на счет",
                "Перевод с карты на карту"
            ]
        ),
        (
            [],  # Проверка на пустой список
            []
        )
    ]
)
def test_transaction_descriptions(transactions, expected_descriptions):
    descriptions = transaction_descriptions(transactions)
    assert list(descriptions) == expected_descriptions

# Параметризованный тест для генератора номеров карт
@pytest.mark.parametrize(
    "start, end, expected_numbers",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005"
            ]
        ),
        (
            100,
            102,
            [
                "0000 0000 0000 0100",
                "0000 0000 0000 0101",
                "0000 0000 0000 0102"
            ]
        ),
        (
            9999999999999990,
            9999999999999999,
            [
                "9999 9999 9999 9990",
                "9999 9999 9999 9991",
                "9999 9999 9999 9992",
                "9999 9999 9999 9993",
                "9999 9999 9999 9994",
                "9999 9999 9999 9995",
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999"
            ]
        ),
        (
            1234567890123456,
            1234567890123456,
            ["1234 5678 9012 3456"]
        )
    ]
)
def test_card_number_generator(start, end, expected_numbers):
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected_numbers
    # Дополнительная проверка формата
    for number in generated_numbers:
        assert len(number) == 19  # 16 цифр + 3 пробела
        assert all(part.isdigit() for part in number.split())
        assert all(len(part) == 4 for part in number.split())
