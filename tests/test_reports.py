from unittest.mock import patch, mock_open
from src.reports import write_reports


def test_write_reports():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        @write_reports("test_file.txt")
        def test_func():
            return "Тестовые данные"

        test_func()

    mock_file.assert_called_once_with("test_file.txt", "a+", encoding="utf-8")
    mock_file().write.assert_called_once_with("Тестовые данные\n")

def test_write_reports_new_file():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        @write_reports()
        def test_func():
            return "Тестовые данные"

        test_func()

    mock_file.assert_called_once_with("doc_for_reports.txt", "a+", encoding="utf-8")
    mock_file().write.assert_called_once_with("Тестовые данные\n")

def test_write_reports_error():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        @write_reports("test_file.txt")
        def test_func():
            raise ValueError("Тестовая ошибка")

        try:
            test_func()
        except ValueError:
            pass

        mock_file().write.assert_called_once_with("Произошла ошибка: Тестовая ошибка\n")

def test_write_reports_error_new_file():
    mock_file = mock_open()
    with patch("builtins.open", mock_file):
        @write_reports("doc_for_reports.txt")
        def test_func():
            raise ValueError("Тестовая ошибка")

        try:
            test_func()
        except ValueError:
            pass

        mock_file().write.assert_called_once_with("Произошла ошибка: Тестовая ошибка\n")
