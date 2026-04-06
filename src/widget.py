from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """
    Маскирует номер карты или счёта в строке с информацией о платеже.

    Args:
        card_info (str): Строка с типом карты/счёта и номером, например:
            "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".

    Returns:
        str: Строка с замаскированным номером.
    """
    parts = card_info.split()
    if not parts:
        raise ValueError("Входная строка не может быть пустой")

    number_str = parts[-1]

    # Проверяем, что номер состоит только из цифр
    if not number_str.isdigit():
        raise ValueError("Номер карты/счёта должен содержать только цифры")

    if card_info.startswith("Счет"):
        masked_number = get_mask_account(number_str)
    else:
        masked_number = get_mask_card_number(number_str)

    return f"{' '.join(parts[:-1])} {masked_number}"


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
