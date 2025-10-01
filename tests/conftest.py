import pytest

# Фикстуры для номеров карт
@pytest.fixture
def valid_card_number():
    return "1234 56** **** 3456"

@pytest.fixture
def max_card_number():
    return "9999 99** **** 9999"

@pytest.fixture
def min_card_number():
    return "1111 11** **** 1111"

@pytest.fixture
def short_card_number():
    return 123456789012345  # 15 цифр

@pytest.fixture
def long_card_number():
    return 12345678901234567  # 17 цифр

@pytest.fixture
def different_card_number():
    return "1234 56** **** 5678"

@pytest.fixture
def reverse_card_number():
    return "8765 43** **** 4321"

# Фикстуры для номеров счетов
@pytest.fixture
def valid_account_number():
    return "**3456"

@pytest.fixture
def min_length_account():
    return "**3456"

@pytest.fixture
def medium_length_account():
    return "**6789"

@pytest.fixture
def long_account():
    return "**9012"

@pytest.fixture
def too_short_account():
    return 12345

@pytest.fixture
def invalid_account():
    return 123


# Фикстуры для filter_by_state
@pytest.fixture
def default_operations():
    return 2

@pytest.fixture
def pending_operations():
    return 2

@pytest.fixture
def no_match_operations():
    return 0

@pytest.fixture
def invalid_operations():
    return []

# Фикстуры для sort_by_date
@pytest.fixture
def unsorted_operations(expected_dates=None):
    return expected_dates

@pytest.fixture
def reverse_sorted_operations():
    return '[op["date"]]'


# Фикстуры для карт
@pytest.fixture(params=[
    ("Карта 1234567890123456", "Карта 1234 56** **** 3456"),
    ("1234567890123456", " 1234 56** **** 3456"),
    ("1234567812345678", " 1234 56** **** 5678"),
    ("9876543210987654", " 9876 54** **** 7654"),
    ("Карта  1234567890123456", "Карта 1234 56** **** 3456"),
    ("Карта1234567890123456", "Карта 1234 56** **** 3456")
])
def card_test_data(request):
    return request.param

# Фикстуры для счетов
@pytest.fixture(params=[
    ("Счет 1234567890123456", "Счет **3456"),
    ("СЧЕТ 1234567890123456", "СЧЕТ **3456"),
    ("счет 1234567890123456", "счет **3456")
])
def account_test_data(request):
    return request.param

# Фикстура для неверного формата
@pytest.fixture
def invalid_input():
    return "Неверный формат 1234"