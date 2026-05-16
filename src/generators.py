"""Модуль с генераторами для обработки транзакций."""

from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты для фильтрации (например, "USD")

    Yields:
        Транзакции, где валюта операции соответствует заданной

    Example:
        >>> transactions = [
        ...     {
        ...         "id": 939719570,
        ...         "operationAmount": {
        ...             "amount": "9824.07",
        ...             "currency": {"name": "USD", "code": "USD"}
        ...         },
        ...         "description": "Перевод организации"
        ...     },
        ...     {
        ...         "id": 142264268,
        ...         "operationAmount": {
        ...             "amount": "79114.93",
        ...             "currency": {"name": "USD", "code": "USD"}
        ...         },
        ...         "description": "Перевод со счета на счет"
        ...     }
        ... ]
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> print(next(usd_transactions)["description"])
        Перевод организации
        >>> print(next(usd_transactions)["description"])
        Перевод со счета на счет
    """
    for transaction in transactions:
        try:
            if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
                yield transaction
        except (AttributeError, KeyError, TypeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций по очереди.

    Args:
        transactions: Список словарей с транзакциями

    Yields:
        Описание каждой операции

    Example:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"},
        ...     {"description": "Перевод с карты на карту"}
        ... ]
        >>> descriptions = transaction_descriptions(transactions)
        >>> print(next(descriptions))
        Перевод организации
        >>> print(next(descriptions))
        Перевод со счета на счет
    """
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            if description:
                yield description
        except (AttributeError, KeyError, TypeError):
            continue


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное значение диапазона
        stop: Конечное значение диапазона (включительно)

    Yields:
        Номера карт в отформатированном виде

    Example:
        >>> for card_number in card_number_generator(1, 3):
        ...     print(card_number)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
    """
    for number in range(start, stop + 1):
        if number < 1 or number > 9999999999999999:
            continue

        # Форматируем номер с ведущими нулями до 16 цифр
        formatted_number = f"{number:016d}"

        # Разбиваем на группы по 4 цифры
        card_number = " ".join(formatted_number[i:i + 4] for i in range(0, 16, 4))

        yield card_number
