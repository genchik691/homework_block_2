from typing import Any, Dict, List, Optional


def filter_by_state(operations: List[Dict[str, Any]], state: Optional[str] = None) -> List[Dict[str, Any]]:
    """Фильтрует операции по статусу."""
    if state is None:
        state = "EXECUTED"
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """Сортирует операции по дате."""
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
