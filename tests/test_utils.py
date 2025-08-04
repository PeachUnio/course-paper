from unittest.mock import patch

import pandas as pd

from src.utils import reading_excel_file


@patch("pandas.read_excel")
def test_reading_excel_file(mock_read_excel):
    test_data = pd.DataFrame({"id": [650703, 3107343], "date": ["EXECUTED", "CANCELED"]})
    mock_read_excel.return_value = test_data

    result = reading_excel_file("succes.csv")
    assert result == [{"id": 650703, "date": "EXECUTED"}, {"id": 3107343, "date": "CANCELED"}]
    mock_read_excel.assert_called_once_with("succes.csv")


def test_reading_excel_file_empty_path():
    result = reading_excel_file("")
    assert result == "Путь не найден"


@patch("pandas.read_excel")
def test_reading_excel_file_error(mock_read_excel):
    mock_read_excel.side_effect = Exception("NotFound")
    result = reading_excel_file("error.csv")
    assert result == "Поизошла ошибка NotFound"
