import json
from collections import defaultdict
from datetime import datetime, timedelta

# from src.utils import reading_excel_file


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


def sort_by_category(transactions, card_number, input_date, period="M"):
    """Обрабатывает данные о расходах за нужный период"""

    start_date, input_date_dt = sort_by_date(input_date, period)

    filtered_transactions = [
        t
        for t in transactions
        if (
            t["Номер карты"] == f"*{str(card_number)[-4:]}"
            and t["Статус"] == "OK"
            and t["Сумма операции"] < 0
            and start_date <= datetime.strptime(t["Дата операции"].split()[0], "%d.%m.%Y").date() <= input_date_dt
        )
    ]

    main_categories = defaultdict(int)
    cash_transfers = defaultdict(int)
    total_expenses = 0.0

    for t in filtered_transactions:
        amount = abs(int(t["Сумма операции"]))
        category = t["Категория"] or "Без категории"

        if category in ["Наличные", "Переводы"]:
            cash_transfers[category] += amount
        else:
            main_categories[category] += amount

        total_expenses += amount

    sorted_main = sorted(main_categories.items(), key=lambda x: x[1], reverse=True)

    top_main = [{"category": k, "amount": v} for k, v in sorted_main[:7]]

    other_amount = sum(v for k, v in sorted_main[7:])
    if other_amount > 0:
        top_main.append({"category": "Остальное", "amount": other_amount})

    sorted_cash = sorted(cash_transfers.items(), key=lambda x: x[1], reverse=True)
    cash_result = [{"category": k, "amount": v} for k, v in sorted_cash]

    # Формируем итоговую структуру
    result = {"total_amount": round(total_expenses, 2), "main": top_main, "transfers_and_cash": cash_result}

    return json.dumps(result, ensure_ascii=False, indent=2, default=str)
