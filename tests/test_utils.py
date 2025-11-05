import pytest
from unittest.mock import Mock, patch
from src.utils import load_transactions


@pytest.fixture
def valid_json_file():
    """Возвращает путь к валидному JSON-файлу (список транзакций)."""
    return "test_transactions_valid.json"


@pytest.fixture
def invalid_json_file():
    """Возвращает путь к невалидному JSON-файлу."""
    return "test_transactions_invalid.json"


@pytest.fixture
def nonexistent_file():
    """Путь к несуществующему файлу."""
    return "nonexistent.json"


@pytest.fixture
def mock_open():
    """Мок для встроенной функции open (эмулирует контекстный менеджер)."""
    with patch("builtins.open", Mock()) as mock:
        yield mock


@pytest.fixture
def mock_os_path_exists():
    """Мок для os.path.exists."""
    with patch("os.path.exists", Mock()) as mock:
        yield mock


# Тест 1: Файл существует, содержит валидный JSON-список
def test_load_valid_json(valid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True

    # Настраиваем мок для файлового объекта
    mock_file = Mock()
    mock_file.read = Mock(return_value="[1, 2, 3]")  # Исправлен JSON

    # Эмулируем контекстный менеджер
    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=False)

    mock_open.return_value = mock_context

    result = load_transactions(valid_json_file)
    assert result == [1, 2, 3]  # Сравниваем с списком


# Тест 2: Файл не существует
def test_file_not_exists(nonexistent_file, mock_os_path_exists):
    mock_os_path_exists.return_value = False

    result = load_transactions(nonexistent_file)
    assert result == []


# Тест 3: Ошибка чтения файла (IOError)
def test_io_error(valid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True
    mock_open.side_effect = IOError("Ошибка чтения файла")

    result = load_transactions(valid_json_file)
    assert result == []


# Тест 4: Невалидный JSON (JSONDecodeError)
def test_json_decode_error(invalid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True

    mock_file = Mock()
    mock_file.read = Mock(return_value="{invalid json}")

    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=False)

    mock_open.return_value = mock_context

    result = load_transactions(invalid_json_file)
    assert result == []


# Тест 5: JSON не является списком (например, словарь)
def test_json_not_list(valid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True

    mock_file = Mock()
    mock_file.read = Mock(return_value='{"key": "value"}')

    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=False)

    mock_open.return_value = mock_context

    result = load_transactions(valid_json_file)
    assert result == []


# Тест 6: Пустой файл
def test_empty_file(valid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True

    mock_file = Mock()
    mock_file.read = Mock(return_value="")

    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=False)

    mock_open.return_value = mock_context

    result = load_transactions(valid_json_file)
    assert result == []


# Тест 7: JSON содержит корректный список строк
def test_valid_list_of_strings(valid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True

    mock_file = Mock()
    mock_file.read = Mock(return_value='["tx1", "tx2", "tx3"]')

    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=False)

    mock_open.return_value = mock_context

    result = load_transactions(valid_json_file)
    assert result == ["tx1", "tx2", "tx3"]


# Тест 8: JSON с одиночным значением (не список)
def test_single_value(valid_json_file, mock_os_path_exists, mock_open):
    mock_os_path_exists.return_value = True

    mock_file = Mock()
    mock_file.read = Mock(return_value='"просто строка"')

    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_file)
    mock_context.__exit__ = Mock(return_value=False)

    mock_open.return_value = mock_context

    result = load_transactions(valid_json_file)
    assert result == []
