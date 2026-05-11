"""Модуль с декораторами для логирования выполнения функций."""

import functools
import os
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функции.

    Логирует имя функции, результат выполнения или ошибку.
    Если filename указан, логи пишутся в файл, иначе выводятся в консоль.

    Args:
        filename: Опциональное имя файла для записи логов

    Returns:
        Декорированная функция

    Example:
        >>> @log(filename="mylog.txt")
        ... def my_function(x, y):
        ...     return x + y
        >>> result = my_function(1, 2)
        >>> print(result)
        3
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = f"{func.__name__} ok"

                # Выводим или записываем в файл
                if filename:
                    _write_to_file(log_message, filename)
                else:
                    print(log_message)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                # Выводим или записываем в файл
                if filename:
                    _write_to_file(error_message, filename)
                else:
                    print(error_message)

                # Перевыбрасываем исключение
                raise

        return wrapper
    return decorator


def _write_to_file(message: str, filename: str) -> None:
    """
    Записывает сообщение в файл с временной меткой.

    Args:
        message: Сообщение для записи
        filename: Имя файла
    """
    # Создаем директорию logs, если её нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Полный путь к файлу
    filepath = os.path.join(log_dir, filename)

    # Добавляем временную метку
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}\n"

    # Записываем в файл
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(formatted_message)


# Альтернативный вариант без сохранения результата в переменную
# для использования в примерах с консольным выводом
if __name__ == "__main__":
    # Пример использования для консоли
    @log()
    def add(a, b):
        return a + b

    add(5, 3)

    # Пример использования с файлом
    @log(filename="example.log")
    def multiply(a, b):
        return a * b

    multiply(4, 5)