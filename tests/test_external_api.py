"""Тесты для модуля external_api."""

from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_currency


class TestConvertCurrency:
    """Тесты для функции convert_currency."""

    @pytest.fixture
    def rub_transaction(self):
        """Фикстура транзакции в рублях."""
        return {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}

    @pytest.fixture
    def usd_transaction(self):
        """Фикстура транзакции в долларах."""
        return {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    @pytest.fixture
    def eur_transaction(self):
        """Фикстура транзакции в евро."""
        return {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}

    def test_convert_rub_transaction(self, rub_transaction):
        """Тест конвертации рублевой транзакции."""
        result = convert_currency(rub_transaction)
        assert result == 1000.50
        assert isinstance(result, float)

    def test_convert_usd_transaction_with_api(self, usd_transaction):
        """Тест конвертации USD с использованием API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 9000.00}

        with patch("src.external_api.requests.get", return_value=mock_response):
            with patch("src.external_api.os.getenv", return_value="fake_api_key"):
                result = convert_currency(usd_transaction)
                assert result == 9000.00

    def test_convert_eur_transaction_with_api(self, eur_transaction):
        """Тест конвертации EUR с использованием API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 9800.00}

        with patch("src.external_api.requests.get", return_value=mock_response):
            with patch("src.external_api.os.getenv", return_value="fake_api_key"):
                result = convert_currency(eur_transaction)
                assert result == 9800.00

    def test_convert_usd_transaction_without_api_key(self, usd_transaction):
        """Тест конвертации USD без API ключа (использует fallback)."""
        with patch("src.external_api.os.getenv", return_value=None):
            result = convert_currency(usd_transaction)
            # Используется fallback курс 90.0
            assert result == 100.00 * 90.0

    def test_convert_eur_transaction_without_api_key(self, eur_transaction):
        """Тест конвертации EUR без API ключа (использует fallback)."""
        with patch("src.external_api.os.getenv", return_value=None):
            result = convert_currency(eur_transaction)
            # Используется fallback курс 98.0
            assert result == 100.00 * 98.0

    def test_convert_transaction_with_api_error(self, usd_transaction):
        """Тест конвертации при ошибке API."""
        mock_response = Mock()
        mock_response.status_code = 500

        with patch("src.external_api.requests.get", return_value=mock_response):
            with patch("src.external_api.os.getenv", return_value="fake_api_key"):
                result = convert_currency(usd_transaction)
                # Используется fallback курс
                assert result == 100.00 * 90.0

    def test_convert_transaction_with_request_exception(self, usd_transaction):
        """Тест конвертации при исключении запроса."""
        with patch("src.external_api.requests.get", side_effect=Exception("Connection error")):
            with patch("src.external_api.os.getenv", return_value="fake_api_key"):
                result = convert_currency(usd_transaction)
                # Используется fallback курс
                assert result == 100.00 * 90.0

    def test_convert_transaction_missing_currency(self):
        """Тест транзакции без валюты."""
        transaction = {"operationAmount": {"amount": "100"}}
        result = convert_currency(transaction)
        # По умолчанию RUB, но т.к. нет кода валюты, вернется 0
        assert result == 0.0

    def test_convert_transaction_invalid_amount(self):
        """Тест транзакции с некорректной суммой."""
        transaction = {"operationAmount": {"amount": "invalid", "currency": {"code": "USD"}}}
        with patch("src.external_api.os.getenv", return_value=None):
            result = convert_currency(transaction)
            assert result == 0.0

    def test_convert_transaction_missing_amount(self):
        """Тест транзакции без суммы."""
        transaction = {"operationAmount": {"currency": {"code": "USD"}}}
        with patch("src.external_api.os.getenv", return_value=None):
            result = convert_currency(transaction)
            assert result == 0.0

    @pytest.mark.parametrize("currency_code,expected_rate", [("USD", 90.0), ("EUR", 98.0)])
    def test_convert_different_currencies_fallback(self, currency_code, expected_rate):
        """Параметризованный тест конвертации разных валют с fallback."""
        transaction = {"operationAmount": {"amount": "100", "currency": {"code": currency_code}}}
        with patch("src.external_api.os.getenv", return_value=None):
            result = convert_currency(transaction)
            assert result == 100 * expected_rate
