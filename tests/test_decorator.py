import pytest
from src.decorators import log


# Основная тестовая функция с декоратором
@log()
def test_function_success():
    return 1 + 1


@log()
def original_test_function_error():  # Изменено имя функции
    return 1 / 0


# Тесты
def test_log_success(capsys):
    result = test_function_success()
    captured = capsys.readouterr()
    assert "test_function_success ok" in captured.err
    assert result == 2


def test_log_error(capsys):
    with pytest.raises(ZeroDivisionError):
        original_test_function_error()  # Используем новое имя
    captured = capsys.readouterr()
    assert "original_test_function_error error: ZeroDivisionError. Inputs: (), {}" in captured.err


# Тест с файлом логов
def test_log_to_file(tmp_path):
    log_file = tmp_path / "test_log.txt"
    filename = str(log_file)

    @log(filename=filename)
    def test_function():  # Используем другое имя
        return 1 + 1

    result = test_function()
    with open(filename, "r") as file:
        content = file.read()
        assert "test_function ok" in content
    assert result == 2


# Новый тест: проверка логов при ошибке
def test_log_error_to_file(tmp_path):
    log_file = tmp_path / "test_log_error.txt"
    filename = str(log_file)

    @log(filename=filename)
    def test_function_error_in_file():  # Новое уникальное имя
        return 1 / 0

    with pytest.raises(ZeroDivisionError):
        test_function_error_in_file()

    with open(filename, "r") as file:
        content = file.read()
        assert "test_function_error_in_file error: ZeroDivisionError. Inputs: (), {}" in content


# Проверка работы декоратора с разными типами аргументов
def test_log_with_args():
    @log()
    def func_with_args(a, b):
        return a + b

    result = func_with_args(2, 3)
    assert result == 5


# Проверка работы декоратора с именованными аргументами
def test_log_with_kwargs():
    @log()
    def func_with_kwargs(a=1, b=2):
        return a * b

    result = func_with_kwargs(a=3, b=4)
    assert result == 12


# Запуск тестов
if __name__ == "__main__":
    pytest.main()
