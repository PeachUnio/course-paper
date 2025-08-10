from src.views import sort_by_date, sort_by_category, sorted_by_receipt, checking_exchange_rate, checking_stock_prices
from src.services import just_search
from src.utils import reading_excel_file
from src.reports import spending_by_category
from dotenv import load_dotenv
import os


def main():
    """Функция, которая собирает логику программы"""
    load_dotenv()
    data = reading_excel_file(os.getenv("EXCEL_PATH"))   # скачиваем таблицу с данными

    # узнаем необходимые данные для работы программы
    print("Приветствуем, уважаемый клиент")
    card_number = input("Введите Ваш номер карты ")
    print("""Введите дату и период за который хотите увидеть данные где 
    W – неделя,
    M – месяц (по умолчанию),
    Y – год,
    All – весь период
    """)
    input_date = input("Введите дату в формате ДД.ММ.ГГГГ: ")
    period = input("Введите период: ")

    # логика работы веб-страницы
    print("Данные отсортированные по самым популярным категориям трат:")
    print(sort_by_category(data, card_number, input_date, period))

    print("Данные о поступлениях на вашу карту:")
    print(sorted_by_receipt(data, card_number, input_date, period))

    print("Для того что бы увидеть курс валют и акции, заполните настройки")  # настройки лежат в user_settings.json
    print("Курс волют:")
    print(checking_exchange_rate())

    print("Акции:")
    print(checking_stock_prices())  # только 5 бесплатных запросов

    # логика работы сервисов
    print(just_search(data, card_number))

    # логика работы отчетов
    now_data = input("""Введите дату до которой хотите узнать траты по категориям, 
    при пропуске данные будут до сегодняшней даты """)
    category = input("Введите категорию по которой хотите получить данные")

    print(spending_by_category(data, card_number, category, now_data))

    print("Спасибо за пользования программой<3")

