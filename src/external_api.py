from dotenv import load_dotenv
import os
import requests
from typing import Any, Dict

# Загружаем переменные окружения
load_dotenv(".env")


def convert_to_rubles(transaction: Dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict): Словарь с полями 'amount' и 'currency'
    Returns:
        float: Сумма в рублях
    """
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", "RUB")

    # Если валюта уже RUB — возвращаем сумму
    if currency == "RUB":
        try:
            return float(amount)
        except (ValueError, TypeError):
            return 0.0

    # Получаем параметры API
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("Не задан API_KEY в переменных окружения")

    try:
        # Формируем URL с динамической валютой
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"

        response = requests.get(url, headers={"apikey": api_key}, timeout=10)
        response.raise_for_status()

        # Используем Any для обработки ответа API
        data: Any = response.json()

        if "rates" not in data:
            raise KeyError("Ответ API не содержит поле 'rates'")

        rates = data.get("rates", {})

        # Проверка наличия курса RUB
        if "RUB" not in rates:
            raise KeyError("В ответе API отсутствует курс RUB")

        rate = rates.get("RUB", 1)

        return float(amount) * rate

    except requests.RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        try:
            return float(amount)  # Повторная попытка конвертировать amount
        except (ValueError, TypeError):
            return 0.0  # Безопасный возврат при неудачной конвертации

    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка обработки ответа API: {e}")
        return 0.0  # Гарантированный безопасный возврат
