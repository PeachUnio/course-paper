import json


def just_search(transactions, card_number):
    """Функция, которая находит транзакции по словам в описании или категории"""
    input_data = input("Ведите слова для поиска ").lower()

    filtered_transaction = [
        t
        for t in transactions
        if (t["Номер карты"] == f"*{str(card_number)[-4:]}")
        and input_data in str(t["Категория"]).lower()
        or input_data in str(t["Описание"].lower())
    ]

    if not filtered_transaction:
        return "Данных по вашему запросу не найдено"
    return json.dumps(filtered_transaction, ensure_ascii=False, indent=2, default=str)
