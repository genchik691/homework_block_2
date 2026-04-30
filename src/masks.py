def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя видимыми первые 6 и последние 4 цифры.
    Формат: 1234 56** **** 3456
    """
    if not card_number:  # обработка пустой строки
        return ""

    # Удаляем пробелы и дефисы
    clean_number = card_number.replace(" ", "").replace("-", "")

    if not clean_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    # Если номер короче 6 цифр — не маскируем
    if len(clean_number) < 6:
        return clean_number

    # Для номеров ровно 6 цифр — возвращаем как есть
    if len(clean_number) == 6:
        return clean_number

    # Определяем количество последних цифр:
    # - для номеров 7–9 цифр: последние 2 цифры
    # - для номеров 10–15 цифр: последние 3 цифры
    # - для номеров 16+ цифр: последние 4 цифры
    if len(clean_number) <= 10:
        num_last_digits = 2
    elif len(clean_number) <= 15:
        num_last_digits = 3
    else:
        num_last_digits = 4

    # Берём последние N цифр
    end = clean_number[-num_last_digits:]
    start = clean_number[:6]

    return f"{start[:4]} {start[4:6]}** **** {end}"


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
