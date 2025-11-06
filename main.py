import logging

from typing import Dict, List

# Импорты модулей проекта
from src.csv_reader import load_csv
from src.excel_reader import load_excel
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card
from utils.bank_processing import process_bank_search

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_format = get_file_format()

    try:
        data = load_data(file_format)

        # Добавляем сообщение о выбранном формате
        if file_format == "json":
            print("Программа: Для обработки выбран JSON-файл.")
        elif file_format == "csv":
            print("Программа: Для обработки выбран CSV-файл.")
        elif file_format == "xlsx":
            print("Программа: Для обработки выбран XLSX-файл.")

    except Exception as e:
        print(f"Программа: Ошибка при загрузке данных: {str(e)}")
        return

    status = get_valid_status()
    filtered_data = filter_by_state(data, status)

    filtered_data = apply_additional_filters(filtered_data)

    display_results(filtered_data)


def get_file_format() -> str:
    while True:
        choice = input("Ваш выбор: ")
        if choice in ["1", "2", "3"]:
            return ["json", "csv", "xlsx"][int(choice) - 1]
        print("Программа: Неверный выбор. Попробуйте снова.")


def load_data(file_format: str) -> List[Dict]:
    try:
        if file_format == "json":
            return load_transactions("data/operations.json")  # Исправлен путь!
        elif file_format == "csv":
            return load_csv("data/transactions.csv")
        elif file_format == "xlsx":
            return load_excel("data/transactions.xlsx")
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных: {str(e)}")
        raise


def get_valid_status() -> str:
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING\n"
        )
        if status.upper() in valid_statuses:
            return status.upper()
        print(f"Программа: Статус операции '{status}' недоступен.")


def apply_additional_filters(data: List[Dict]) -> List[Dict]:
    if input_yes_no("Программа: Отсортировать операции по дате? "):
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        # Исправлено: передаём корректный аргумент, который ожидает sort_by_date
        data = sort_by_date(data, descending=(order == "по убыванию"))

    if input_yes_no("Программа: Выводить только рублевые транзакции? "):
        data = [tx for tx in data if tx.get("currency", "").upper() == "RUB"]

    if input_yes_no("Программа: Отфильтровать список транзакций по определенному слову в описании? "):
        search_term = input("Программа: Введите слово для поиска:\n").strip()
        data = process_bank_search(data, search_term)

    return data


def input_yes_no(prompt: str) -> bool:
    while True:
        response = input(prompt).strip().lower()
        if response in ["да", "yes"]:
            return True
        elif response in ["нет", "no"]:
            return False
        print("Программа: Введите 'Да' или 'Нет'")


def display_results(data: List[Dict]):
    if not data:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    print("Программа: Распечатываю итоговый список транзакций...")
    print(f"Программа: Всего банковских операций в выборке: {len(data)}\n")

    for idx, transaction in enumerate(data, start=1):
        try:
            # Форматируем дату
            formatted_date = get_date(transaction.get("date", ""))

            # Получаем основные данные
            description = transaction.get("description", "")
            from_account = mask_account_card(transaction.get("from", ""))
            to_account = mask_account_card(transaction.get("to", ""))
            amount = transaction.get("amount", 0)

            # Выводим информацию о транзакции
            print(f"Операция №{idx}")
            print(f"Дата: {formatted_date}")
            print(f"Описание: {description}")
            print(f"От: {from_account}")
            print(f"До: {to_account}")

            # Извлекаем сумму и валюту из operationAmount
            amount = transaction.get("operationAmount", {}).get("amount", "N/A")
            currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name", "N/A")
            print(f"Сумма: {amount} {currency_name}\n")

        except Exception as e:
            logger.error(f"Ошибка при выводе транзакции: {str(e)}")
            print("Программа: Ошибка при выводе данных транзакции")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма: Работа завершена по запросу пользователя.")
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
        print("Программа: Произошла непредвиденная ошибка.")
