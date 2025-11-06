from unittest.mock import mock_open, patch

import pytest

from src.csv_reader import load_csv


# Базовый тест с корректными данными (разделитель ;)
@patch("builtins.open", new_callable=mock_open, read_data="id;state;date;amount\n1;EXECUTED;2023-01-01;1000")
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
@patch("builtins.open", new_callable=mock_open, read_data="id;date\n1;2023-01-01")
def test_load_csv_missing_columns(mock_file):
    result = load_csv("incomplete.csv")
    assert len(result) == 1
    assert "state" not in result[0]
    assert "amount" not in result[0]


# Тест на некорректные данные
@patch("builtins.open", new_callable=mock_open, read_data="id;state;date;amount\n1;EXECUTED;invalid_date;abc")
def test_load_csv_invalid_data(mock_file):
    result = load_csv("invalid.csv")
    assert result[0]["amount"] == "abc"  # Проверка, что данные не преобразуются автоматически


# Тест на кодировку
@patch("builtins.open", new_callable=mock_open, read_data="id;state;date;amount\n1;EXECUTED;2023-01-01;1000")
def test_load_csv_encoding(mock_file):
    mock_file.encoding = "utf-8"
    result = load_csv("encoded.csv")
    assert result[0]["id"] == "1"


# Тест на большие числа
@patch("builtins.open", new_callable=mock_open, read_data="id;state;date;amount\n1;EXECUTED;2023-01-01;1000000000")
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


# Тест на разные типы данных в колонках
@patch("builtins.open", new_callable=mock_open, read_data="id;state;date;amount\n1;EXECUTED;2023-01-01;1000.50")
def test_load_csv_float_values(mock_file):
    result = load_csv("float_values.csv")
    assert result[0]["amount"] == "1000.50"


# Тест на спецсимволы в данных
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="id;state;description\n1;EXECUTED;Описание с символами: @#$%^&*()",
)
def test_load_csv_special_chars(mock_file):
    result = load_csv("special_chars.csv")
    assert result[0]["description"] == "Описание с символами: @#$%^&*()"


# Тест на длинные строки
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=(
        "id;description\n"
        "1;Очень длинное описание, которое превышает "
        "стандартную длину строки и содержит много информации"
    ),
)
def test_load_csv_long_strings(mock_file):
    result = load_csv("long_strings.csv")
    assert len(result[0]["description"]) > 50


# Тест на пустые значения
@patch("builtins.open", new_callable=mock_open, read_data="id;state;date;amount\n1;;2023-01-01;")
def test_load_csv_empty_values(mock_file):
    result = load_csv("empty_values.csv")
    assert result[0]["state"] == ""
    assert result[0]["amount"] == ""


# Тест на разные типы кавычек
@patch("builtins.open", new_callable=mock_open, read_data='id;state;description\n1;EXECUTED;"Описание в кавычках"')
def test_load_csv_quoted_values(mock_file):
    result = load_csv("quoted_values.csv")
    assert result[0]["description"] == "Описание в кавычках"


# Тест на большое количество строк
@patch(
    "builtins.open", new_callable=mock_open, read_data="id;state\n" + "\n".join([f"{i};EXECUTED" for i in range(1000)])
)
def test_load_csv_large_file(mock_file):
    result = load_csv("large_file.csv")
    assert len(result) == 1000


# Тест на смешанный формат данных
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="id;state;date;amount\n1;EXECUTED;2023-01-01;1000\n2;PENDING;2023-02-01;2000.50",
)
def test_load_csv_mixed_data(mock_file):
    result = load_csv("mixed_data.csv")
    assert result[0]["amount"] == "1000"
    assert result[1]["amount"] == "2000.50"
