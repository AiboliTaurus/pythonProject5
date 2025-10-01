import pytest


from src.masks import get_mask_card_number, get_mask_account


# Тесты для get_mask_card_number
# Параметризация для валидных тестов
@pytest.mark.parametrize(
    "input_number, expected_result",
    [
        (1234567890123456, "1234 56** **** 3456"),  # базовый случай
        (9999999999999999, "9999 99** **** 9999"),  # все девятки
        (1111111111111111, "1111 11** **** 1111"),  # все единицы
        (1234567812345678, "1234 56** **** 5678"),  # разные цифры
        (8765432187654321, "8765 43** **** 4321")   # обратный порядок
    ]
)
def test_get_mask_card_number_valid(input_number, expected_result):
    result = get_mask_card_number(input_number)
    assert result == expected_result

# Параметризация для невалидных длин
@pytest.mark.parametrize(
    "invalid_number",
    [
        123456789012345,   # 15 цифр
        12345678901234567  # 17 цифр
    ]
)
def test_get_mask_card_number_invalid_length(invalid_number):
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_number)




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