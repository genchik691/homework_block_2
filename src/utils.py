"""Модуль с утилитами для работы с JSON файлами."""

import json
from pathlib import Path
from typing import Any, Dict, List, Union


def read_json_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с транзакциями.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список в случае ошибки или если файл содержит не список.

    Examples:
        >>> # Создаем временный файл для примера
        >>> import tempfile
        >>> import json
        >>> test_data = [{"id": 1, "description": "Test transaction"}]
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        ...     json.dump(test_data, tmp)
        ...     tmp_path = tmp.name
        >>> transactions = read_json_file(tmp_path)
        >>> len(transactions)
        1
        >>> transactions[0]["description"]
        'Test transaction'
        >>> # Очищаем временный файл
        >>> import os
        >>> os.unlink(tmp_path)
    """
    try:
        # Преобразуем путь к файлу
        file_path = Path(file_path)

        # Проверяем существование файла
        if not file_path.exists():
            return []

        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if isinstance(data, list):
            return data
        else:
            return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError):
        return []
