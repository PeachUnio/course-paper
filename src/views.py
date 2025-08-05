from datetime import datetime, timedelta
from src.utils import reading_excel_file


def sort_by_date(input_day, period="M"):
    """Функция, принимающая на вход дату и периуд и возвращающаяя диапозон дат за этот периуд"""
    date = datetime.strptime(input_day, "%d.%m.%Y")

    if period == "W":
        start = date - timedelta(days=date.weekday())
    if period == "M":
        start = date.replace(day=1)
    if period == "Y":
        start = date.replace(month=1, day=1)
    if period == "ALL":
        start = datetime.min

    return start.date(), date.date()

def sort_by_category(data_dict, card_number, category):
    """Функция, которая фильтрует операции по категории трат"""
    sorted_transactions = []
    for i in data_dict:
        if i["Номер карты"] == f"*{str(card_number)[-4:]}":
            sorted_transactions.append(i)

    category_sorted = []
    for tr in sorted_transactions:
        if tr["Категория"] == category:
            category_sorted.append(tr)
    return category_sorted
