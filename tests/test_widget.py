import pytest
from src.widget import mask_account_card


def test_mask_account_card_card():
    # Карта с текстом
    assert mask_account_card("Карта 1234567890123456") == "Карта 1234 56** **** 3456"

    # Только номер карты (добавляем пробел в ожидаемый результат)
    assert mask_account_card("1234567890123456") == " 1234 56** **** 3456"

    # Дополнительные тесты
    assert mask_account_card("1234567812345678") == " 1234 56** **** 5678"
    assert mask_account_card("9876543210987654") == " 9876 54** **** 7654"

    # Проверка на разные случаи
    assert mask_account_card("Карта  1234567890123456") == "Карта 1234 56** **** 3456"  # с лишними пробелами
    assert mask_account_card("Карта1234567890123456") == "Карта 1234 56** **** 3456"  # без пробела после слова Карта


def test_mask_account_card_account():
    # Счет с текстом
    assert mask_account_card("Счет 1234567890123456") == "Счет **3456"

    # Разные варианты написания "счет"
    assert mask_account_card("СЧЕТ 1234567890123456") == "СЧЕТ **3456"
    assert mask_account_card("счет 1234567890123456") == "счет **3456"


def test_mask_account_card_invalid():
    # Неверный формат номера
    with pytest.raises(ValueError):
        mask_account_card("Неверный формат 1234")