import pytest
from unittest.mock import patch, mock_open
from src.csv_reader import load_csv


# Базовый тест с корректными данными
@patch("builtins.open", new_callable=mock_open, read_data="id,state,date,amount\n1,EXECUTED,2023-01-01,1000")
def test_load_csv_basic(mock_file):
    result = load_csv("dummy.csv")
    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert result[0]["amount"] == "1000"


# Тест на пустой файл
@patch("builtins.open", new_callable=mock_open, read_data="")
def test_load_csv_empty_file(mock_file):
    result = load_csv("empty.csv")
    assert result == []


# Тест на отсутствующие столбцы
@patch("builtins.open", new_callable=mock_open, read_data="id,date\n1,2023-01-01")
def test_load_csv_missing_columns(mock_file):
    result = load_csv("incomplete.csv")
    assert len(result) == 1
    assert "state" not in result[0]
    assert "amount" not in result[0]


# Тест на некорректные данные
@patch("builtins.open", new_callable=mock_open, read_data="id,state,date,amount\n1,EXECUTED,invalid_date,abc")
def test_load_csv_invalid_data(mock_file):
    result = load_csv("invalid.csv")
    assert result[0]["amount"] == "abc"  # Проверка, что данные не преобразуются автоматически


# Тест на кодировку
@patch("builtins.open", new_callable=mock_open, read_data="id,state,date,amount\n1,EXECUTED,2023-01-01,1000")
def test_load_csv_encoding(mock_file):
    mock_file.encoding = "utf-8"
    result = load_csv("encoded.csv")
    assert result[0]["id"] == "1"


# Тест на большие числа
@patch("builtins.open", new_callable=mock_open, read_data="id,state,date,amount\n1,EXECUTED,2023-01-01,1000000000")
def test_load_csv_large_numbers(mock_file):
    result = load_csv("large_numbers.csv")
    assert result[0]["amount"] == "1000000000"


# Тест на отсутствие файла
def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv("nonexistent.csv")


# Тест на некорректный путь
def test_load_csv_invalid_path():
    with pytest.raises(FileNotFoundError):
        load_csv("/invalid/path/file.csv")
