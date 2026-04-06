import re
from datetime import datetime
from src.masks import get_mask_card_number, get_mask_account



def mask_account_card(text: str) -> str:
    """
    Маскирует номер карты или счёта в тексте.

    Args:
        text (str): Строка с типом карты/счёта и номером, например:
            'Visa Platinum 7000792289606361' или 'Счёт 73654108430135874305'

    Returns:
        str: Строка с замаскированным номером.
    """
    # Ищем 16‑значный номер карты
    card_match = re.search(r'\b\d{16}\b', text)
    if card_match:
        card_number = card_match.group()
        masked_number = get_mask_card_number(card_number)
        return re.sub(r'\d{16}', masked_number, text)

    # Ищем длинный номер счёта (20 цифр)
    account_match = re.search(r'\b\d{20}\b', text)
    if account_match:
        account_number = account_match.group()
        masked_number = get_mask_account(account_number)
        return re.sub(r'\d{20}', masked_number, text)

    return text



def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): Дата в формате '2024-03-11T02:26:18.671407'

    Returns:
        str: Дата в формате '11.03.2024'
    """
    # Парсим дату из строки ISO
    dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    # Форматируем в нужный формат
    return dt.strftime('%d.%m.%Y')