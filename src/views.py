from datetime import datetime, timedelta


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
