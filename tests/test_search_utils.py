"""Тесты для модуля search_utils."""

import pytest

from src.search_utils import count_transactions_by_categories, search_transactions


class TestSearchTransactions:
    """Тесты для функции search_transactions."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с образцами транзакций."""
        return [
            {"id": 1, "description": "Перевод организации", "amount": 1000},
            {"id": 2, "description": "Перевод со счета на счет", "amount": 2000},
            {"id": 3, "description": "Оплата услуг", "amount": 500},
            {"id": 4, "description": "Перевод с карты на карту", "amount": 1500},
            {"id": 5, "description": "Покупка в магазине", "amount": 300},
        ]

    def test_search_existing_string(self, sample_transactions):
        """Тест поиска существующей строки."""
        result = search_transactions(sample_transactions, "Перевод")
        assert len(result) == 3
        assert all("Перевод" in t["description"] for t in result)

    def test_search_case_insensitive(self, sample_transactions):
        """Тест регистронезависимого поиска."""
        result = search_transactions(sample_transactions, "перевод")
        assert len(result) == 3

        result = search_transactions(sample_transactions, "ПЕРЕВОД")
        assert len(result) == 3

    def test_search_not_found(self, sample_transactions):
        """Тест поиска отсутствующей строки."""
        result = search_transactions(sample_transactions, "Несуществующее")
        assert result == []

    def test_search_empty_list(self):
        """Тест с пустым списком."""
        result = search_transactions([], "Перевод")
        assert result == []

    def test_search_empty_string(self, sample_transactions):
        """Тест с пустой строкой поиска."""
        result = search_transactions(sample_transactions, "")
        assert result == []

    @pytest.mark.parametrize("search_string,expected_count", [
        ("перевод", 3),
        ("оплата", 1),
        ("покупка", 1),
        ("услуг", 1),
        ("карту", 1),
    ])
    def test_search_parametrized(self, sample_transactions, search_string, expected_count):
        """Параметризованный тест поиска."""
        result = search_transactions(sample_transactions, search_string)
        assert len(result) == expected_count


class TestCountTransactionsByCategories:
    """Тесты для функции count_transactions_by_categories."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с образцами транзакций."""
        return [
            {"id": 1, "description": "Перевод организации", "amount": 1000},
            {"id": 2, "description": "Перевод со счета на счет", "amount": 2000},
            {"id": 3, "description": "Оплата услуг", "amount": 500},
            {"id": 4, "description": "Перевод с карты на карту", "amount": 1500},
            {"id": 5, "description": "Покупка в магазине", "amount": 300},
        ]

    def test_count_categories(self, sample_transactions):
        """Тест подсчета категорий."""
        categories = ["Перевод", "Оплата", "Покупка"]
        result = count_transactions_by_categories(sample_transactions, categories)

        assert result["Перевод"] == 3
        assert result["Оплата"] == 1
        assert result["Покупка"] == 1

    def test_case_insensitive_count(self, sample_transactions):
        """Тест регистронезависимого подсчета."""
        categories = ["перевод", "ОПЛАТА", "Покупка"]
        result = count_transactions_by_categories(sample_transactions, categories)

        assert result["перевод"] == 3
        assert result["ОПЛАТА"] == 1

    def test_categories_not_found(self, sample_transactions):
        """Тест с категориями, которых нет."""
        categories = ["Несуществующая", "Другая"]
        result = count_transactions_by_categories(sample_transactions, categories)

        assert result["Несуществующая"] == 0
        assert result["Другая"] == 0

    def test_empty_transactions(self):
        """Тест с пустым списком транзакций."""
        categories = ["Перевод", "Оплата"]
        result = count_transactions_by_categories([], categories)

        assert result["Перевод"] == 0
        assert result["Оплата"] == 0

    def test_empty_categories(self, sample_transactions):
        """Тест с пустым списком категорий."""
        result = count_transactions_by_categories(sample_transactions, [])
        assert result == {}

    def test_transaction_without_description(self):
        """Тест транзакции без описания."""
        transactions = [
            {"id": 1, "description": "Перевод"},
            {"id": 2, "description": ""},
            {"id": 3},
        ]
        categories = ["Перевод"]
        result = count_transactions_by_categories(transactions, categories)

        assert result["Перевод"] == 1
