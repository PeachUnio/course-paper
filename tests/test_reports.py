from unittest.mock import patch, mock_open
import pytest
import json
from src.reports import write_reports, spending_by_category


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

@pytest.fixture
def test_data():
    return [
        {
            "Дата операции": "16.07.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -50.9,
            "Категория": "Красота",
            "Описание": "Улыбка радуги",
        },
        {
            "Дата операции": "28.12.2021",
            "Номер карты": "*5091",
            "Статус": "OK",
            "Сумма операции": -348.7,
            "Категория": "Каршеринг",
            "Описание": "Ситидрайв",
        },
        {
            "Дата операции": "24.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": 20000.00,
            "Категория": "Другое",
            "Описание": "Иван Д.",
        },
        {
            "Дата операции": "14.06.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -776.9,
            "Категория": "Красота",
            "Описание": "Подружка",
        },
        {
            "Дата операции": "18.01.2018",
            "Номер карты": "*8533",
            "Статус": "OK",
            "Сумма операции": -210.0,
            "Категория": "Фастфуд",
            "Описание": "Бургеркинг",
        },
        {
            "Дата операции": "20.01.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -124.9,
            "Категория": "Красота",
            "Описание": "Улыбка радуги",
        },
    ]

@pytest.fixture
def test_result():
    return [
        {
            "Дата операции": "16.07.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -50.9,
            "Категория": "Красота",
            "Описание": "Улыбка радуги",
        },
        {
            "Дата операции": "14.06.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -776.9,
            "Категория": "Красота",
            "Описание": "Подружка",
        }
    ]

def test_spending_by_category(test_data, test_result):
    result = spending_by_category(test_data, 21123317197, "Красота", "25.07.2021")
    assert result == json.dumps(test_result, ensure_ascii=False, indent=2, default=str)

def test_spending_by_category_void(test_data):
    result = spending_by_category(test_data, 21123317197, "Красота")
    assert result == "Не найдено трат по заданным условиям"

@pytest.fixture
def test_error_data():
    return [
        {
            "Дата операции": "16.07.2021",
            "Сумма операции": -50.9,
            "Категория": "Красота",
            "Описание": "Улыбка радуги",
        },
        {
            "Дата операции": "14.06.2021",
            "Сумма операции": -776.9,
            "Категория": "Красота",
            "Описание": "Подружка",
        }
    ]

def test_spending_by_category_error(test_error_data):
    result = spending_by_category(test_error_data, 4473773748, "Нет")
    assert result == "Произошла ошибка 'Номер карты'"
