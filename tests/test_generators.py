"""Тесты для модуля generators."""

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions():
    """Фикстура с образцами транзакций."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    @pytest.mark.parametrize(
        "currency,expected_count",
        [
            ("USD", 3),  # В примере выше 3 транзакции в USD
            ("RUB", 2),
            ("EUR", 0),
        ],
    )
    def test_filter_by_currency_parametrized(self, sample_transactions, currency, expected_count):
        """Параметризованный тест фильтрации по разным валютам."""
        filtered = filter_by_currency(sample_transactions, currency)
        result = list(filtered)
        assert len(result) == expected_count

        if expected_count > 0:
            for transaction in result:
                assert transaction["operationAmount"]["currency"]["code"] == currency

    def test_filter_by_currency_empty_list(self):
        """Тест с пустым списком транзакций."""
        filtered = filter_by_currency([], "USD")
        result = list(filtered)
        assert result == []

    def test_filter_by_currency_no_matching_currency(self, sample_transactions):
        """Тест когда нет транзакций в нужной валюте."""
        filtered = filter_by_currency(sample_transactions, "EUR")
        result = list(filtered)
        assert result == []

    def test_filter_by_currency_returns_iterator(self, sample_transactions):
        """Тест что функция возвращает итератор."""
        result = filter_by_currency(sample_transactions, "USD")
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_filter_by_currency_invalid_data(self):
        """Тест с некорректными данными."""
        invalid_data = [
            {"id": 1},  # нет operationAmount
            {"operationAmount": "invalid"},  # некорректный тип
            None,  # None вместо словаря
        ]
        filtered = filter_by_currency(invalid_data, "USD")
        # Функция должна обработать ошибки и вернуть пустой итератор
        result = list(filtered)
        assert result == []


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    @pytest.mark.parametrize(
        "transaction_data,expected",
        [
            ([{"description": "Перевод организации"}], ["Перевод организации"]),
            (
                [{"description": "Перевод 1"}, {"description": "Перевод 2"}, {"description": "Перевод 3"}],
                ["Перевод 1", "Перевод 2", "Перевод 3"],
            ),
        ],
    )
    def test_transaction_descriptions_parametrized(self, transaction_data, expected):
        """Параметризованный тест получения описаний."""
        descriptions = transaction_descriptions(transaction_data)
        result = list(descriptions)
        assert result == expected

    def test_transaction_descriptions_with_sample_data(self, sample_transactions):
        """Тест с реальными данными."""
        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        descriptions = transaction_descriptions(sample_transactions)
        result = list(descriptions)
        assert result == expected_descriptions

    def test_transaction_descriptions_empty_list(self):
        """Тест с пустым списком."""
        descriptions = transaction_descriptions([])
        result = list(descriptions)
        assert result == []

    def test_transaction_descriptions_missing_description(self):
        """Тест когда отсутствует описание."""
        transactions = [
            {"id": 1, "description": "Есть описание"},
            {"id": 2},  # нет поля description
            {"id": 3, "description": ""},  # пустое описание
        ]
        expected = ["Есть описание"]  # пустые и отсутствующие описания пропускаем
        descriptions = transaction_descriptions(transactions)
        result = list(descriptions)
        assert result == expected

    def test_transaction_descriptions_returns_generator(self, sample_transactions):
        """Тест что функция возвращает генератор."""
        result = transaction_descriptions(sample_transactions)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize(
        "start,stop,expected",
        [
            (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
            (5, 7, ["0000 0000 0000 0005", "0000 0000 0000 0006", "0000 0000 0000 0007"]),
            (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]),
            (9999999999999995, 9999999999999996, ["9999 9999 9999 9995", "9999 9999 9999 9996"]),
        ],
    )
    def test_card_number_generator_range(self, start, stop, expected):
        """Параметризованный тест генерации номеров карт в диапазоне."""
        result = list(card_number_generator(start, stop))
        assert result == expected

    def test_card_number_generator_format(self):
        """Тест правильности форматирования."""
        result = list(card_number_generator(1, 1))
        assert result[0] == "0000 0000 0000 0001"
        assert " " in result[0]

        # Проверяем что номер состоит из 4 групп по 4 цифры
        groups = result[0].split()
        assert len(groups) == 4
        assert all(len(group) == 4 for group in groups)
        assert all(group.isdigit() for group in groups)

    def test_card_number_generator_single_value(self):
        """Тест генерации одного номера."""
        result = list(card_number_generator(42, 42))
        assert result == ["0000 0000 0000 0042"]

    def test_card_number_generator_large_numbers(self):
        """Тест с большими числами в конце диапазона."""
        result = list(card_number_generator(9999999999999999, 9999999999999999))
        assert result == ["9999 9999 9999 9999"]

    def test_card_number_generator_returns_generator(self):
        """Тест что функция возвращает генератор."""
        result = card_number_generator(1, 5)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")
