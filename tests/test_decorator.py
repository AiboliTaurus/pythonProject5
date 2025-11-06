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
    # Создаем временный файл лога
    log_file = tmp_path / "test_log.txt"

    # Открываем файл для записи
    with open(log_file, "w") as f:
        # Записываем тестовое сообщение
        f.write("Тестовый лог-файл")

    # Проверяем, что файл создан и содержит данные
    assert log_file.exists()
    assert log_file.read_text() == "Тестовый лог-файл"

    # Дополнительно можно проверить размер файла
    assert log_file.stat().st_size > 0


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
