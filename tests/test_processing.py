from src.processing import filter_by_state, sort_by_date

# Пример входных данных
operations = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def test_filter_by_state_default() -> None:
    result = filter_by_state(operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_cancelled() -> None:
    result = filter_by_state(operations, "CANCELED")
    assert len(result) == 2
    assert all(op["state"] == "CANCELED" for op in result)


def test_sort_by_date_desc() -> None:
    result = sort_by_date(operations)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_asc() -> None:
    result = sort_by_date(operations, reverse=False)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates)
