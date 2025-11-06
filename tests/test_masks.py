import pytest

from src.masks import get_mask_account, get_mask_card_number


# Тесты для get_mask_card_number
def test_get_mask_card_number_valid():
    # Базовый тест
    assert get_mask_card_number(1234567890123456) == "1234 56** **** 3456"

    # Граничные случаи
    assert get_mask_card_number(9999999999999999) == "9999 99** **** 9999"
    assert get_mask_card_number(1111111111111111) == "1111 11** **** 1111"


def test_get_mask_card_number_invalid_length():
    # Слишком короткий номер
    with pytest.raises(ValueError):
        get_mask_card_number(123456789012345)  # 15 цифр

    # Слишком длинный номер
    with pytest.raises(ValueError):
        get_mask_card_number(12345678901234567)  # 17 цифр


def test_get_mask_card_number_edge_cases():
    # Разные комбинации цифр
    assert get_mask_card_number(1234567812345678) == "1234 56** **** 5678"
    assert get_mask_card_number(8765432187654321) == "8765 43** **** 4321"


# Тесты для get_mask_account
def test_get_mask_account_valid():
    # Базовый тест
    assert get_mask_account(1234567890123456) == "**3456"

    # Минимальная длина
    assert get_mask_account(123456) == "**3456"

    # Разные длины
    assert get_mask_account(123456789) == "**6789"
    assert get_mask_account(123456789012) == "**9012"


def test_get_mask_account_invalid_length():
    # Слишком короткий номер
    with pytest.raises(ValueError):
        get_mask_account(12345)  # 5 цифр

    # Некорректные входные данные
    with pytest.raises(ValueError):
        get_mask_account(123)  # 3 цифры
