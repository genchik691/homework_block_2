"""Модуль для поиска и подсчета операций с использованием регулярных выражений."""

import re
from collections import Counter
from typing import Any, Dict, List


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по строке в описании с использованием регулярных выражений.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска (регистронезависимо)

    Returns:
        Список транзакций, в описании которых найдена искомая строка

    Example:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"},
        ...     {"description": "Оплата услуг"}
        ... ]
        >>> result = search_transactions(transactions, "перевод")
        >>> len(result)
        2
    """
    if not transactions or not search_string:
        return []

    # Составляем регулярное выражение (регистронезависимый поиск)
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Фильтруем транзакции
    result = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def count_transactions_by_categories(
        transactions: List[Dict[str, Any]],
        categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций по категориям на основе описания.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством транзакций по каждой категории

    Example:
        >>> transactions = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"},
        ...     {"description": "Оплата услуг"}
        ... ]
        >>> categories = ["Перевод", "Оплата"]
        >>> result = count_transactions_by_categories(transactions, categories)
        >>> result["Перевод"]
        2
    """
    if not transactions or not categories:
        return {category: 0 for category in categories}

    # Создаем счетчик
    counter = Counter()

    # Для каждой транзакции проверяем, к какой категории она относится
    for transaction in transactions:
        description = transaction.get("description", "")
        if not description:
            continue

        # Проверяем каждую категорию
        for category in categories:
            # Регистронезависимый поиск
            if re.search(re.escape(category), description, re.IGNORECASE):
                counter[category] += 1
                break  # Считаем транзакцию только в первой подходящей категории

    # Возвращаем результат для всех запрошенных категорий
    result = {category: counter.get(category, 0) for category in categories}
    return result
