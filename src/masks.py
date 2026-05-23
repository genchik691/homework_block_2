"""Модуль для маскирования номеров карт и счетов."""

import logging
import sys
from pathlib import Path

# Добавляем путь к src для доктестов
sys.path.insert(0, str(Path(__file__).parent))

# Пытаемся импортировать logger_config, если не получается, создаем базовый логер
try:
    from logger_config import setup_logger
except ImportError:
    # Для доктестов создаем простой логер
    def setup_logger(name, log_file, level=logging.DEBUG):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        return logger

# Настраиваем логер для модуля masks
logger = setup_logger(__name__, "masks.log", logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Args:
        card_number: Номер карты (строка из 16 цифр, может содержать пробелы или дефисы)

    Returns:
        Замаскированный номер карты в формате XXXX XX** **** XXXX

    Example:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
        >>> get_mask_card_number("1234-5678-9012-3456")
        '1234 56** **** 3456'
        >>> get_mask_card_number("")
        ''
    """
    logger.debug(f"Маскирование номера карты: {card_number}")

    # Пустая строка возвращается как есть
    if card_number == "":
        logger.info("Пустая строка, возвращаем как есть")
        return ""

    # Проверяем, что номер карты - строка
    if not isinstance(card_number, str):
        error_msg = f"Номер карты должен быть строкой, получен {type(card_number)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверяем, есть ли в строке только цифры, пробелы и дефисы
    # Если есть другие символы - выбрасываем исключение
    allowed_chars = set("0123456789- ")
    if not all(c in allowed_chars for c in card_number):
        error_msg = f"Номер карты должен содержать только цифры, получен: {card_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Удаляем пробелы и дефисы
    cleaned_number = card_number.replace(" ", "").replace("-", "")

    # Если после очистки нет цифр - исключение
    if not cleaned_number:
        error_msg = f"Номер карты должен содержать только цифры, получен: {card_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Для коротких номеров (меньше 16 цифр) маскируем с учетом длины
    if len(cleaned_number) < 16:
        # Определяем сколько цифр показывать в конце
        if len(cleaned_number) <= 6:
            # Очень короткий номер - возвращаем как есть
            result = cleaned_number
        elif len(cleaned_number) <= 10:
            # Показываем последние 2 цифры
            result = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-2:]}"
        else:
            # Показываем последние 3 цифры
            result = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-3:]}"

        logger.info(f"Успешно замаскирован короткий номер карты: {result}")
        return result

    # Для полного 16-значного номера
    result = f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
    logger.info(f"Успешно замаскирован номер карты: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета.

    Args:
        account_number: Номер счета (строка)

    Returns:
        Замаскированный номер счета в формате **XXXX для длинных номеров,
        или исходный номер для коротких

    Example:
        >>> get_mask_account("73654108430135874305")
        '**4305'
        >>> get_mask_account("9999")
        '9999'
        >>> get_mask_account("12")
        '12'
    """
    logger.debug(f"Маскирование номера счета: {account_number}")

    # Проверяем, что номер счета - строка
    if not isinstance(account_number, str):
        error_msg = f"Номер счета должен быть строкой, получен {type(account_number)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Проверяем, есть ли в строке только цифры
    if not account_number.isdigit():
        error_msg = f"Номер счета должен содержать только цифры, получен: {account_number}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Если номер пустой или очень короткий (меньше 4 цифр), возвращаем как есть
    if len(account_number) <= 4:
        logger.info(f"Короткий номер счета ({len(account_number)} цифр), возвращаем без изменений")
        return account_number

    # Для длинных номеров показываем только последние 4 цифры
    masked = f"**{account_number[-4:]}"
    logger.info(f"Успешно замаскирован номер счета: {masked}")
    return masked