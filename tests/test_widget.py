import pytest
from src.widget import mask_account_card
from src.widget import get_date


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


# Тест на некорректные номера
def test_mask_account_card_invalid_numbers():
    # Слишком короткий номер
    with pytest.raises(ValueError):
        mask_account_card("Карта 1234")

    # Буквы в номере
    with pytest.raises(ValueError):
        mask_account_card("Карта 1234ABCD")

    # Специальные символы
    with pytest.raises(ValueError):
        mask_account_card("Карта 1234$%^&*")


# Тест на номера с пробелами в начале/конце
def test_mask_account_card_whitespace():
    assert mask_account_card(" Карта 1234567890123456 ") == "Карта 1234 56** **** 3456"
    assert mask_account_card(" Счет 1234567890123456 ") == "Счет **3456"


# Базовый тест для корректной даты
def test_get_date_valid():
    date_str = "2023-10-30T12:34:56"
    expected = "30.10.2023"
    result = get_date(date_str)
    assert result == expected


# Тест для минимальной допустимой даты
def test_get_date_min_date():
    date_str = "1970-01-01T00:00:00"
    expected = "01.01.1970"
    result = get_date(date_str)
    assert result == expected


# Тест для максимальной допустимой даты
def test_get_date_max_date():
    date_str = "9999-12-31T23:59:59"
    expected = "31.12.9999"
    result = get_date(date_str)
    assert result == expected


# Тест для даты с часовым поясом
def test_get_date_with_timezone():
    date_str = "2023-10-30T12:34:56+03:00"
    expected = "30.10.2023"
    result = get_date(date_str)
    assert result == expected


# Тест для даты с Z (UTC)
def test_get_date_utc():
    date_str = "2023-10-30T12:34:56Z"
    expected = "30.10.2023"
    result = get_date(date_str)
    assert result == expected


# Тест для даты с микросекундами
def test_get_date_microseconds():
    date_str = "2023-10-30T12:34:56.123456"
    expected = "30.10.2023"
    result = get_date(date_str)
    assert result == expected
