"""Модуль для чтения финансовых операций из CSV и Excel файлов."""

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd

# Добавляем корень проекта в путь Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logger_config import setup_logger

# Настраиваем логер для модуля file_reader
logger = setup_logger(__name__, "file_reading.log", logging.DEBUG)


def read_csv_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает CSV файл с транзакциями и возвращает список словарей.

    Args:
        file_path: Путь к CSV файлу

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список в случае ошибки.

    Example:
        transactions = read_csv_file("data/transactions.csv")
        len(transactions)
        5
    """
    logger.debug(f"Попытка чтения CSV файла: {file_path}")

    try:
        # Преобразуем путь к файлу
        file_path = Path(file_path)

        # Проверяем существование файла
        if not file_path.exists():
            logger.error(f"CSV файл не найден: {file_path}")
            return []

        # Читаем CSV файл с использованием pandas
        df = pd.read_csv(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')

        # Обрабатываем NaN значения
        for transaction in transactions:
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV файла {file_path}")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error(f"CSV файл пуст: {file_path}")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV файла {file_path}: {e}")
        return []


def read_excel_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает Excel файл с транзакциями и возвращает список словарей.

    Args:
        file_path: Путь к Excel файлу (.xlsx)

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список в случае ошибки.

    Example:
        transactions = read_excel_file("data/transactions_excel.xlsx")
        len(transactions)
        5
    """
    logger.debug(f"Попытка чтения Excel файла: {file_path}")

    try:
        # Преобразуем путь к файлу
        file_path = Path(file_path)

        # Проверяем существование файла
        if not file_path.exists():
            logger.error(f"Excel файл не найден: {file_path}")
            return []

        # Читаем Excel файл с использованием pandas
        df = pd.read_excel(file_path, engine='openpyxl')

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict(orient='records')

        # Обрабатываем NaN значения
        for transaction in transactions:
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel файла {file_path}")
        return transactions

    except pd.errors.EmptyDataError:
        logger.error(f"Excel файл пуст: {file_path}")
        return []
    except ValueError as e:
        logger.error(f"Ошибка при чтении Excel файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel файла {file_path}: {e}")
        return []
