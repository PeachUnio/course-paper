import json
from pathlib import Path

import pandas as pd


def reading_excel_file(excel_path):
    """Функция, которая читает данные из excel-файла"""
    try:
        if excel_path:
            excel_data = pd.read_excel(excel_path)
            return excel_data.to_dict("records")
        else:
            return "Путь не найден"
    except Exception as e:
        return f"Поизошла ошибка {e}"


def load_users_settings():
    """Функция, которая загружает настройки пользователя из JSON-файла"""
    try:
        dir_path = Path(__file__).parent.parent
        settings_path = dir_path / "user_settings.json"

        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return f"Поизошла ошибка"
