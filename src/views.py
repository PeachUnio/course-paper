import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

from src.utils import load_users_settings, reading_excel_file


def sort_by_date(input_day, period="M"):
    """Функция, принимающая на вход дату и период и возвращающая диапазон дат за этот период"""
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

    result = {"total_amount": round(total_expenses, 2), "main": top_main, "transfers_and_cash": cash_result}

    return json.dumps(result, ensure_ascii=False, indent=2, default=str)


def sorted_by_receipt(transactions, card_number, input_date, period="M"):
    """Функция, которая сортирует поступления на карту"""

    start_date, input_date_dt = sort_by_date(input_date, period)

    filtered_transactions = [
        t
        for t in transactions
        if (
            t["Номер карты"] == f"*{str(card_number)[-4:]}"
            and t["Статус"] == "OK"
            and t["Сумма операции"] > 0
            and start_date <= datetime.strptime(t["Дата операции"].split()[0], "%d.%m.%Y").date() <= input_date_dt
        )
    ]

    categories = defaultdict(int)
    total_expenses = 0

    for t in filtered_transactions:
        amount = int(t["Сумма операции"])
        category = t["Категория"]

        categories[category] += amount
        total_expenses += amount

    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    category_result = [{"category": k, "amount": v} for k, v in sorted_categories]

    result = {"total_amount": total_expenses, "main": category_result}

    return json.dumps(result, ensure_ascii=False, indent=2, default=str)


def checking_exchange_rate():
    """Функция, которая проверяет курс валют из настроек пользователя"""
    try:
        settings = load_users_settings().get("user_currencies", [])

        if not settings:
            return "Настройки не добавлены"

        load_dotenv()
        api_key = os.getenv("API_CURRENCIES")
        if not api_key:
            return "API ключ не найден"

        url = "https://api.apilayer.com/exchangerates_data/latest"
        headers = {"apikey": api_key}
        params = {"base": "RUB", "symbols": ",".join(settings)}

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        rates = data.get("rates", {})
        result = [{"currency": curr, "rate": round(1 / rate, 2)} for curr, rate in rates.items()]
        return json.dumps(result, ensure_ascii=False, indent=2, default=str)

    except Exception:
        return "Произошла ошибка"


def checking_stock_prices():
    """Функция, которая проверяет акции из настроек пользователя"""
    settings = load_users_settings().get("user_stocks", [])

    if not settings:
        return "Настройки не добавлены"

    load_dotenv()
    api_key = os.getenv("API_STOCK")
    if not api_key:
        return "API ключ не найден"

    results = []

    url = "https://www.alphavantage.co/query"
    # бесплатно можно сделать только 5 запросов
    for stock in settings:
        try:
            params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": api_key}
            response = requests.get(url, params=params)

            results.append({"stock": stock, "price": float(response.json()["Global Quote"]["05. price"])})

        except Exception:
            return "Произошла ошибка"
    return json.dumps(results, ensure_ascii=False, indent=2, default=str)


print(checking_stock_prices())
