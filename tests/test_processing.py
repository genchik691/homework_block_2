from typing import Any, Dict, List, Optional

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """Предоставляет тестовые данные для операций."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def edge_case_operations() -> Dict[str, List[Dict[str, Any]]]:
    """Предоставляет данные для тестирования граничных случаев."""
    return {
        "empty": [],
        "single_executed": [{"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000000"}],
        "single_cancelled": [{"id": 2, "state": "CANCELED", "date": "2023-01-02T00:00:00.000000"}],
    }


@pytest.mark.parametrize(
    "state_filter,expected_count,expected_state",
    [
        (None, 2, "EXECUTED"),
        ("EXECUTED", 2, "EXECUTED"),
        ("CANCELED", 2, "CANCELED"),
    ],
)
def test_filter_by_state(
    sample_operations: List[Dict[str, Any]], state_filter: Optional[str], expected_count: int, expected_state: str
) -> None:
    """Тестирует фильтрацию операций по статусу."""
    result = filter_by_state(sample_operations, state_filter)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(op["state"] == expected_state for op in result)


def test_filter_by_state_edge_cases(edge_case_operations: Dict[str, List[Dict[str, Any]]]) -> None:
    """Тестирует фильтрацию с граничными случаями."""
    # Пустой список
    result_empty = filter_by_state(edge_case_operations["empty"], "EXECUTED")
    assert result_empty == []

    # Один элемент — EXECUTED
    result_single = filter_by_state(edge_case_operations["single_executed"], "EXECUTED")
    assert len(result_single) == 1
    assert result_single[0]["state"] == "EXECUTED"


def test_sort_by_date(sample_operations: List[Dict[str, Any]]) -> None:
    """Тестирует сортировку операций по дате."""
    # Сортировка по возрастанию (старые сначала)
    sorted_asc = sort_by_date(sample_operations)
    dates_asc = [op["date"] for op in sorted_asc]
    assert dates_asc == sorted(dates_asc)  # проверяем, что даты отсортированы

    # Сортировка по убыванию (новые сначала)
    sorted_desc = sort_by_date(sample_operations, reverse=True)
    dates_desc = [op["date"] for op in sorted_desc]
    assert dates_desc == sorted(dates_desc, reverse=True)
