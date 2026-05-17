"""Модуль для работы с внешними API (конвертация валют)."""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


def convert_currency(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Если транзакция в USD или EUR, получает курс через API и конвертирует.
    Если транзакция в RUB, возвращает сумму как есть.

    Args:
        transaction: Словарь с данными транзакции

    Returns:
        Сумма в рублях (float)
    """
    try:
        # Получаем информацию о транзакции
        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("code")

        # Если нет валюты, возвращаем 0
        if currency is None:
            return 0.0

        # Преобразуем сумму в float
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            amount = 0.0

        # Если валюта уже рубли, возвращаем сумму
        if currency == "RUB":
            return amount

        # Если валюта USD или EUR, конвертируем
        if currency in ["USD", "EUR"]:
            return _get_converted_amount(amount, currency)

        # Для других валют возвращаем 0
        return 0.0

    except (KeyError, TypeError, ValueError):
        return 0.0


def _get_converted_amount(amount: float, currency: str) -> float:
    """
    Получает конвертированную сумму через внешнее API.

    Args:
        amount: Сумма в исходной валюте
        currency: Код валюты (USD или EUR)

    Returns:
        Сумма в рублях
    """
    # Оборачиваем ВСЁ в try-except, чтобы гарантированно вернуть значение
    try:
        # Получаем API ключ из переменных окружения
        api_key = os.getenv("EXCHANGE_API_KEY")

        # Если нет API ключа, используем fallback
        if not api_key:
            return _get_fallback_rate(amount, currency)

        # Пытаемся выполнить запрос
        url = "https://api.apilayer.com/exchangerates_data/convert"
        params = {"to": "RUB", "from": currency, "amount": amount}
        headers = {"apikey": api_key}

        # Выполняем запрос (может выбросить исключение)
        response = requests.get(url, params=params, headers=headers, timeout=10)

        # Проверяем статус ответа
        if response.status_code == 200:
            data = response.json()
            result = data.get("result")
            if result is not None:
                return float(result)

        # Если что-то пошло не так, используем fallback
        return _get_fallback_rate(amount, currency)

    except Exception as e:
        # При ЛЮБОМ исключении (сетевая ошибка, таймаут, ошибка парсинга JSON и т.д.)
        # используем fallback курс
        print(f"API error: {e}, using fallback rate")  # Для отладки
        return _get_fallback_rate(amount, currency)


def _get_fallback_rate(amount: float, currency: str) -> float:
    """
    Возвращает конвертированную сумму по приблизительному курсу.

    Args:
        amount: Сумма в исходной валюте
        currency: Код валюты (USD или EUR)

    Returns:
        Сумма в рублях
    """
    # Примерные курсы валют
    rates = {"USD": 90.0, "EUR": 98.0}

    rate = rates.get(currency, 90.0)  # По умолчанию курс USD
    return amount * rate
