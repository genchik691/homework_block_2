from datetime import datetime
from typing import Dict, List


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует список операций по статусу.

    Args:
        operations (List[Dict]): Список словарей с данными о банковских операциях.
        state (str, optional): Статус для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        List[Dict]: Отфильтрованный список операций.
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате.

    Args:
        operations (List[Dict]): Список словарей с данными о банковских операциях.
        reverse (bool, optional): Порядок сортировки. По умолчанию True (убывание).

    Returns:
        List[Dict]: Отсортированный список операций.
    """

    def parse_date(date_str: str) -> datetime:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    return sorted(operations, key=lambda x: parse_date(x["date"]), reverse=reverse)
