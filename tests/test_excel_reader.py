import pandas as pd
import pytest
from unittest.mock import patch
from src.excel_reader import load_excel


# Базовый тест с корректными данными
@pytest.fixture
def mock_excel():
    df = pd.DataFrame(
        {
            "id": [1],
            "state": ["EXECUTED"],
            "date": ["2023-01-01"],
            "amount": [1000],
            "currency_name": ["Рубль"],
            "currency_code": ["RUB"],
            "from": ["Счет 123"],
            "to": ["Счет 456"],
            "description": ["Перевод"],
        }
    )
    return df


def test_load_excel_basic(mock_excel):
    with patch("pandas.read_excel", return_value=mock_excel):
        result = load_excel("test.xlsx")
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["state"] == "EXECUTED"


# Тест на пустой файл
def test_load_excel_empty():
    with patch("pandas.read_excel", return_value=pd.DataFrame()):
        result = load_excel("empty.xlsx")
        assert result == []


# Тест на отсутствующие столбцы
def test_load_excel_missing_columns():
    mock_df = pd.DataFrame({"id": [1], "date": ["2023-01-01"]})
    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("incomplete.xlsx")
        assert len(result) == 1
        assert "state" not in result[0]
        assert "amount" not in result[0]


# Тест на некорректные данные
def test_load_excel_invalid_data():
    mock_df = pd.DataFrame({"id": ["abc"], "amount": ["xyz"]})
    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("invalid.xlsx")
        assert result[0]["id"] == "abc"
        assert result[0]["amount"] == "xyz"


# Тест на большие числа
def test_load_excel_large_numbers():
    mock_df = pd.DataFrame({"id": [1], "amount": [1000000000]})
    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("large_numbers.xlsx")
        assert result[0]["amount"] == 1000000000


# Тест на отсутствие файла
def test_load_excel_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_excel("nonexistent.xlsx")


# Тест на некорректный путь
def test_load_excel_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_excel("/invalid/path/file.xlsx")


# Тест на разные форматы дат
def test_load_excel_date_formats():
    mock_df = pd.DataFrame({"date": ["2023-01-01", "01/01/2023", "01.01.2023"]})
    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("date_formats.xlsx")
        assert len(result) == 3


# Тест на разные валюты
def test_load_excel_currencies():
    mock_df = pd.DataFrame({"currency_name": ["Рубль", "Доллар", "Евро"], "currency_code": ["RUB", "USD", "EUR"]})

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("dummy.xlsx")

        # Проверка количества записей
        assert len(result) == 3

        # Проверка значений первой записи
        assert result[0]["currency_name"] == "Рубль"
        assert result[0]["currency_code"] == "RUB"

        # Проверка значений второй записи
        assert result[1]["currency_name"] == "Доллар"
        assert result[1]["currency_code"] == "USD"

        # Проверка значений третьей записи
        assert result[2]["currency_name"] == "Евро"
        assert result[2]["currency_code"] == "EUR"

        # Проверка типов данных
        assert isinstance(result, list)
        assert all(isinstance(item, dict) for item in result)

        # Проверка структуры данных
        for item in result:
            assert set(item.keys()) == {"currency_name", "currency_code"}
            assert all(value is not None for value in item.values())


# Тест на наличие пустых листов
def test_load_excel_empty_sheet():
    mock_df = pd.DataFrame()

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("empty_sheet.xlsx")
        assert result == []


# Тест на множественные листы
def test_load_excel_multiple_sheets():
    mock_df = pd.DataFrame({"id": [1, 2], "state": ["EXECUTED", "PENDING"], "date": ["2023-01-01", "2023-01-02"]})

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("multiple_sheets.xlsx")
        assert len(result) == 2


# Тест на наличие формул в Excel
def test_load_excel_formulas():
    mock_df = pd.DataFrame(
        {"id": [1], "calculated_amount": [1000], "formula_cell": ["=A1+B1"]}  # предположим, что это результат формулы
    )

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("formulas.xlsx")
        assert result[0]["calculated_amount"] == 1000


# Тест на наличие объединенных ячеек
def test_load_excel_merged_cells():
    mock_df = pd.DataFrame({"merged_column": ["Значение", None], "id": [1, 2]})

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("merged_cells.xlsx")
        assert result[0]["merged_column"] == "Значение"
        assert result[1]["merged_column"] is None


# Тест на наличие комментариев к ячейкам
def test_load_excel_cell_comments():
    mock_df = pd.DataFrame({"id": [1], "comment": ["Это комментарий к транзакции"]})

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("comments.xlsx")
        assert "comment" in result[0]


# Тест на наличие защищенного файла
def test_load_excel_protected_file():
    with pytest.raises(Exception):
        load_excel("protected.xlsx")


# Тест на наличие условного форматирования
def test_load_excel_conditional_formatting():
    mock_df = pd.DataFrame({"id": [1], "status": ["EXECUTED"]})  # предположим, что форматирование зависит от статуса

    with patch("pandas.read_excel", return_value=mock_df):
        result = load_excel("conditional_formatting.xlsx")
        assert result[0]["status"] == "EXECUTED"
