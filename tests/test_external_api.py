import pytest
from unittest.mock import patch, Mock

import requests

from src.external_api import convert_to_rubles  # замените на реальный путь к модулю


@pytest.fixture
def valid_transaction():
    return {"amount": 100, "currency": "USD"}


@pytest.fixture
def rub_transaction():
    return {"amount": 500, "currency": "RUB"}


@pytest.fixture
def invalid_transaction():
    return {"amount": "invalid", "currency": "EUR"}


@pytest.fixture
def missing_currency_transaction():
    return {"amount": 100}


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock:
        yield mock


# Тест 1: Конвертация из USD в RUB (успешный случай)
def test_convert_usd_to_rub(valid_transaction, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_requests_get.return_value = mock_response

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(valid_transaction)
        assert result == pytest.approx(100 * 90.5)


# Тест 2: Валюта уже RUB (без конвертации)
def test_currency_is_rub(rub_transaction):
    result = convert_to_rubles(rub_transaction)
    assert result == 500.0


# Тест 3: Отсутствие API_KEY (вызывает ValueError)
def test_missing_api_key(valid_transaction):
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="Не задан API_KEY в переменных окружения"):
            convert_to_rubles(valid_transaction)


# Тест 4: Ошибка запроса к API (возвращает исходную сумму)
def test_api_request_failure(valid_transaction, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException("Connection error")

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(valid_transaction)
        assert result == 100.0  # исходная сумма


# Тест 5: Ответ API без поля "rates" (KeyError)
def test_api_response_missing_rates(valid_transaction, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "no rates"}
    mock_requests_get.return_value = mock_response

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(valid_transaction)
        assert result == 0.0  # исходная сумма


# Тест 6: В ответе API нет курса RUB (KeyError)
def test_api_response_missing_rub_rate(valid_transaction, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"USD": 1.0}}  # нет RUB
    mock_requests_get.return_value = mock_response

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(valid_transaction)
        assert result == 0.0  # исходная сумма


# Тест 7: Некорректное значение amount (ValueError)
def test_invalid_amount(invalid_transaction, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_requests_get.return_value = mock_response

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(invalid_transaction)
        assert result == 0.0  # по умолчанию при ошибке


# Тест 8: Отсутствует поле currency (используется RUB по умолчанию)
def test_missing_currency(missing_currency_transaction):
    result = convert_to_rubles(missing_currency_transaction)
    assert result == 100.0  # amount без конвертации


# Тест 9: Таймаут запроса (RequestException)
def test_request_timeout(valid_transaction, mock_requests_get):
    mock_requests_get.side_effect = requests.Timeout("Request timed out")

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(valid_transaction)
        assert result == 100.0  # исходная сумма


# Тест 10: HTTP-ошибка от API (например, 404)
def test_http_error_from_api(valid_transaction, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_requests_get.return_value = mock_response

    with patch.dict("os.environ", {"API_KEY": "test_key"}):
        result = convert_to_rubles(valid_transaction)
        assert result == 100.0  # исходная сумма
