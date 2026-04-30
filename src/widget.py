import re
from datetime import datetime


def mask_account_card(card_info: str) -> str:
    """Маскирует номер карты или счёта в зависимости от длины и формата."""
    card_info = card_info.strip()

    if not card_info:
        raise ValueError("Входная строка не может быть пустой")

    # Извлекаем числовую часть
    number_match = re.search(r"\d+", card_info)
    if not number_match:
        raise ValueError("Номер карты/счёта должен содержать только цифры")

    number = number_match.group()

    # Определяем тип по длине числа
    if len(number) == 16:
        # Карта: маскируем средние цифры
        masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        # Вставляем замаскированное число обратно в строку
        return re.sub(r"\d+", masked_number, card_info)
    elif len(number) >= 4:
        # Счёт: показываем только последние 4 цифры
        masked_number = f"**{number[-4:]}"
        return re.sub(r"\d+", masked_number, card_info)
    else:
        raise ValueError("Некорректная длина номера карты/счёта")


def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): Дата в формате "2024-03-11T02:26:18.671407".

    Returns:
        str: Дата в формате "ДД.ММ.ГГГГ".
    """
    dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y")
