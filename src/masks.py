def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры.
    Формат: 1234 56** **** 3456
    """
    clean_number = card_number.replace(" ", "")

    if len(clean_number) != 16 or not clean_number.isdigit():
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Форматируем с пробелами: 1234 5678 9012 3456
    formatted = f"{clean_number[:4]} {clean_number[4:8]}" f"{clean_number[8:12]} {clean_number[12:]}"

    # Маскируем средние цифры: 1234 56** **** 3456 (убираем лишний пробел)
    masked = f"{formatted[:7]}** **** {formatted[-4:]}"
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта, оставляя видимыми последние 4 цифры.
    Формат: **7890
    """
    clean_number = account_number.replace(" ", "")

    if not clean_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")

    # Для счёта показываем только последние 4 цифры, остальные заменяем на *
    # Но не более 2 звёздочек в начале (согласно ожидаемому результату теста)
    if len(clean_number) > 4:
        # Оставляем только 2 звёздочки в начале + последние 4 цифры
        masked = "**" + clean_number[-4:]
    else:
        masked = clean_number
    return masked
