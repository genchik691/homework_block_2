"""Модуль с утилитами для работы с JSON файлами."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

from src.logger_config import setup_logger

# Настраиваем логер для модуля utils
logger = setup_logger(__name__, "utils.log", logging.DEBUG)


def read_json_file(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Читает JSON файл и возвращает список словарей с транзакциями.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        Список словарей с данными транзакций.
        Возвращает пустой список в случае ошибки или если файл содержит не список.
    """
    logger.debug(f"Попытка чтения JSON файла: {file_path}")

    try:
        # Преобразуем путь к файлу
        file_path = Path(file_path)

        # Проверяем существование файла
        if not file_path.exists():
            logger.error(f"Файл не найден: {file_path}")
            return []

        # Открываем и читаем файл
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")
            return data
        else:
            logger.error(f"Файл {file_path} содержит не список, а {type(data).__name__}")
            return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {file_path}. Ошибка: {e}")
        return []
    except PermissionError as e:
        logger.error(f"Нет прав для чтения файла {file_path}: {e}")
        return []
    except OSError as e:
        logger.error(f"Ошибка операционной системы при чтении файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении файла {file_path}: {e}")
        return []
