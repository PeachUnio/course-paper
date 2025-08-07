import json
import unittest
from datetime import date
from unittest.mock import Mock, patch

from src.views import checking_exchange_rate, checking_stock_prices, sort_by_date


class TestSortByDate(unittest.TestCase):

    def test_sort_by_date_w(self):
        start, end = sort_by_date("18.01.2024", "W")
        self.assertEqual(start, date(2024, 1, 15))
        self.assertEqual(end, date(2024, 1, 18))

    def test_sort_by_date_m(self):
        start, end = sort_by_date("15.05.2023")
        self.assertEqual(start, date(2023, 5, 1))
        self.assertEqual(end, date(2023, 5, 15))

    def test_sort_by_date_y(self):
        start, end = sort_by_date("13.10.2022", "Y")
        self.assertEqual(start, date(2022, 1, 1))
        self.assertEqual(end, date(2022, 10, 13))


class TestCheckingExchangeRate(unittest.TestCase):

    def test_checking_exchange_rate(self):
        with (
            patch.dict("os.environ", {"API_CURRENCIES": "test_key"}),
            patch("src.utils.load_users_settings") as mock_load,
            patch("requests.get") as mock_get,
        ):

            mock_load.return_value = {"user_currencies": ["USD", "EUR"]}
            mock_response = Mock()
            mock_response.json.return_value = {"success": True, "rates": {"USD": 0.013, "EUR": 0.011}}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = checking_exchange_rate()
            expected_result = json.dumps(
                [{"currency": "USD", "rate": 76.92}, {"currency": "EUR", "rate": 90.91}], indent=2
            )

            assert result == expected_result
            mock_get.assert_called_once()

    def test_checking_exchange_rate_error(self):
        with patch.dict("os.environ", {"API_CURRENCIES": ""}), patch("src.utils.load_users_settings") as mock_load:

            mock_load.return_value = {"user_currencies": ["USD", "EUR"]}
            result = checking_exchange_rate()

            assert result == "API ключ не найден"

    def test_checking_stock_prices(self):
        with (
            patch.dict("os.environ", {"API_STOCK": "test_key"}),
            patch("src.utils.load_users_settings") as mock_load,
            patch("requests.get") as mock_get,
        ):

            mock_load.return_value = {"user_stocks": ["AAPL"]}
            mock_response = Mock()
            mock_response.json.return_value = {"Global Quote": {"05. price": "175.50"}}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = checking_stock_prices()
            print(result)

            assert result == '[\n  {\n    "stock": "AAPL",\n    "price": 175.5\n  }\n]'

            mock_get.assert_called_once()

    def test_checking_stock_prices_error(self):
        with patch.dict("os.environ", {"API_STOCK": ""}), patch("src.utils.load_users_settings") as mock_load:

            mock_load.return_value = {"user_stocks": ["AAPL"]}
            result = checking_stock_prices()

            assert result == "API ключ не найден"
