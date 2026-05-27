"""Тесты для модуля processing."""

from typing import Any, Dict, List, Optional

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """Фикстура с образцами операций."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.mark.parametrize(
    "state_filter,expected_count,expected_state",
    [
        (None, 4, None),  # None - возвращаем все транзакции
        ("EXECUTED", 2, "EXECUTED"),
        ("CANCELED", 2, "CANCELED"),
    ],
)
def test_filter_by_state(
    sample_operations: List[Dict[str, Any]],
    state_filter: Optional[str],
    expected_count: int,
    expected_state: Optional[str]
) -> None:
    """Тестирует фильтрацию операций по статусу."""
    result = filter_by_state(sample_operations, state_filter)
    assert len(result) == expected_count

    if expected_state:
        assert all(op["state"] == expected_state for op in result)


def test_filter_by_state_edge_cases(sample_operations: List[Dict[str, Any]]) -> None:
    """Тестирует граничные случаи фильтрации."""
    # Пустой список
    assert filter_by_state([], "EXECUTED") == []
    assert filter_by_state([], None) == []

    # Список без ключа state
    transactions = [{"id": 1}, {"id": 2, "state": "EXECUTED"}]
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2

    # Несуществующий статус
    result = filter_by_state(sample_operations, "PENDING")
    assert result == []

    # Проверка с None (должен вернуть все транзакции)
    result = filter_by_state(sample_operations, None)
    assert len(result) == 4


def test_sort_by_date(sample_operations: List[Dict[str, Any]]) -> None:
    """Тестирует сортировку операций по дате."""
    # Сортировка по возрастанию (старые сначала)
    sorted_asc = sort_by_date(sample_operations, reverse=False)
    dates_asc = [op["date"] for op in sorted_asc]
    # Проверяем, что даты отсортированы по возрастанию
    assert dates_asc == sorted(dates_asc)

    # Сортировка по убыванию (новые сначала)
    sorted_desc = sort_by_date(sample_operations, reverse=True)
    dates_desc = [op["date"] for op in sorted_desc]
    # Проверяем, что даты отсортированы по убыванию
    assert dates_desc == sorted(dates_desc, reverse=True)

    # Проверяем конкретный порядок для возрастающей сортировки
    expected_asc_dates = [
        "2018-06-30T02:08:58.425572",
        "2018-09-12T21:27:25.241689",
        "2018-10-14T08:21:33.419441",
        "2019-07-03T18:35:29.512364"
    ]
    assert dates_asc == expected_asc_dates

    # Пустой список
    assert sort_by_date([]) == []

    # Список без дат
    no_dates = [{"id": 1}, {"id": 2}]
    assert sort_by_date(no_dates) == []
