import unittest
from datetime import date

from src.views import sort_by_date


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
