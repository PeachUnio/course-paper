import json
from datetime import datetime
from functools import wraps


# Декоратор, который записывает результаты функции в заданный файл или создает новый
def write_reports(filename=None):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            file_to_write = filename if filename is not None else "doc_for_reports.txt"
            try:
                result = func(*args, **kwargs)
                with open(file_to_write, "a+", encoding="utf-8") as f:
                    f.write(str(result) + "\n")

            except Exception as e:
                with open(file_to_write, "a+", encoding="utf-8") as f:
                    f.write(f"Произошла ошибка: {str(e)}\n")
                raise

        return inner

    return wrapper


def spending_by_category(transactions, card_number, category, date=None):
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    end_date = datetime.strptime(date, "%d.%m.%Y") if date is not None else datetime.now()
    start_date = end_date.replace(month=end_date.month - 3)

    try:
        sorted_transactions = [
            t
            for t in transactions
            if (
                t["Номер карты"] == f"*{str(card_number)[-4:]}"
                and t["Статус"] == "OK"
                and t["Сумма операции"] < 0
                and start_date <= datetime.strptime(t["Дата операции"].split()[0], "%d.%m.%Y") <= end_date
                and t["Категория"] == category
            )
        ]
        if sorted_transactions:
            return json.dumps(sorted_transactions, ensure_ascii=False, indent=2, default=str)
        else:
            return "Не найдено трат по заданным условиям"

    except Exception as e:
        return f"Произошла ошибка {e}"
