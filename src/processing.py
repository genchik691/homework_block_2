"""Модуль для обработки данных (фильтрация, сортировка)."""

from typing import Any, Dict, List, Optional


def filter_by_state(transactions: List[Dict[str, Any]], state: Optional[str] = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Args:
        transactions: Список словарей с транзакциями
        state: Статус для фильтрации. Если None, возвращает все транзакции

    Returns:
        Отфильтрованный список транзакций

    Example:
        >>> transactions = [
        ...     {"state": "EXECUTED"},
        ...     {"state": "CANCELED"},
        ...     {"state": "EXECUTED"}
        ... ]
        >>> len(filter_by_state(transactions, "EXECUTED"))
        2
    """
    if not transactions:
        return []

    # Если state не указан или None, возвращаем все транзакции
    if state is None:
        return transactions

    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions: Список словарей с транзакциями
        reverse: Если True, сортировка по убыванию (сначала новые).
                 Если False, сортировка по возрастанию (сначала старые)

    Returns:
        Отсортированный список транзакций

    Example:
        >>> transactions = [
        ...     {"date": "2020-01-01"},
        ...     {"date": "2019-01-01"},
        ...     {"date": "2021-01-01"}
        ... ]
        >>> sorted_asc = sort_by_date(transactions, reverse=False)
        >>> sorted_asc[0]["date"]
        '2019-01-01'
    """
    if not transactions:
        return []

    # Фильтруем транзакции без даты
    valid_transactions = [t for t in transactions if t.get("date")]

    # Сортируем
    return sorted(
        valid_transactions,
        key=lambda x: x.get("date", ""),
        reverse=reverse
    )


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.

    Args:
        transactions: Список словарей с транзакциями
        currency: Код валюты (например, "USD", "RUB")

    Returns:
        Отфильтрованный список транзакций
    """
    if not transactions:
        return []

    return [
        t for t in transactions
        if t.get("operationAmount", {}).get("currency", {}).get("code") == currency
    ]


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по описанию (регистронезависимо).

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска в описании

    Returns:
        Отфильтрованный список транзакций
    """
    if not transactions or not search_string:
        return transactions if transactions else []

    search_lower = search_string.lower()
    return [
        t for t in transactions
        if search_lower in t.get("description", "").lower()
    ]
