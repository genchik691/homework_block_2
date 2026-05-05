"""Тесты для модуля decorators."""

import os
import tempfile
from pathlib import Path

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log."""

    @pytest.fixture
    def temp_log_file(self):
        """Фикстура для временного файла логов."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
            tmp_path = tmp.name
        yield tmp_path
        # Очистка после теста
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    @pytest.fixture
    def clean_logs_dir(self):
        """Фикстура для очистки директории logs после тестов."""
        yield
        logs_dir = Path("logs")
        if logs_dir.exists():
            for file in logs_dir.glob("*.txt"):
                file.unlink()
            logs_dir.rmdir()

    def test_log_to_console_success(self, capsys):
        """Тест логирования успешного выполнения в консоль."""

        @log()
        def add(a, b):
            return a + b

        result = add(3, 5)

        captured = capsys.readouterr()
        assert "add ok" in captured.out
        assert result == 8

    def test_log_to_console_error(self, capsys):
        """Тест логирования ошибки в консоль."""

        @log()
        def divide(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out
        assert "Inputs: (10, 0)" in captured.out

    def test_log_to_file_success(self, temp_log_file, clean_logs_dir):
        """Тест логирования успешного выполнения в файл."""

        @log(filename=temp_log_file)
        def multiply(a, b):
            return a * b

        result = multiply(4, 7)

        # Проверяем содержимое файла
        with open(temp_log_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "multiply ok" in content
        assert result == 28

    def test_log_to_file_error(self, temp_log_file, clean_logs_dir):
        """Тест логирования ошибки в файл."""

        @log(filename=temp_log_file)
        def divide(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Проверяем содержимое файла
        with open(temp_log_file, "r", encoding="utf-8") as f:
            content = f.read()

        assert "divide error: ZeroDivisionError" in content
        assert "Inputs: (10, 0)" in content

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (5, 7, 12),
        (10, -3, 7),
        (0, 0, 0),
    ])
    def test_log_with_multiple_inputs(self, capsys, a, b, expected):
        """Параметризованный тест с разными входными данными."""

        @log()
        def add(a, b):
            return a + b

        result = add(a, b)

        captured = capsys.readouterr()
        assert "add ok" in captured.out
        assert result == expected

    def test_log_preserves_function_metadata(self):
        """Тест сохранения метаданных оригинальной функции."""

        @log()
        def my_function(x, y):
            """Моя функция."""
            return x + y

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "Моя функция."

    def test_log_with_kwargs(self, capsys):
        """Тест логирования с именованными аргументами."""

        @log()
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")

        captured = capsys.readouterr()
        assert "greet ok" in captured.out
        assert result == "Hi, Alice!"

    def test_log_multiple_calls_same_file(self, temp_log_file):
        """Тест множественных вызовов в один файл."""

        @log(filename=temp_log_file)
        def add(a, b):
            return a + b

        add(1, 2)
        add(3, 4)
        add(5, 6)

        with open(temp_log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 3
        assert all("add ok" in line for line in lines)

    def test_log_complex_function(self, capsys):
        """Тест логирования сложной функции."""

        @log()
        def process_list(items):
            return [x * 2 for x in items]

        result = process_list([1, 2, 3, 4, 5])

        captured = capsys.readouterr()
        assert "process_list ok" in captured.out
        assert result == [2, 4, 6, 8, 10]

    def test_log_without_filename_creates_no_file(self):
        """Тест что без filename файл не создается."""

        @log()
        def my_func():
            return 42

        logs_dir = Path("logs")
        before_files = set(logs_dir.glob("*.txt")) if logs_dir.exists() else set()

        my_func()

        after_files = set(logs_dir.glob("*.txt")) if logs_dir.exists() else set()

        # Количество файлов не должно увеличиться (учитывая возможные другие тесты)
        assert len(before_files) == len(after_files)