"""Тесты для модуля utils."""

import json
import tempfile
from pathlib import Path

import pytest

from src.utils import read_json_file


class TestReadJsonFile:
    """Тесты для функции read_json_file."""

    @pytest.fixture
    def valid_transactions(self):
        """Фикстура с валидными транзакциями."""
        return [
            {"id": 1, "amount": 100, "currency": "USD"},
            {"id": 2, "amount": 200, "currency": "EUR"},
            {"id": 3, "amount": 300, "currency": "RUB"},
        ]

    @pytest.fixture
    def temp_json_file(self, valid_transactions):
        """Фикстура для временного JSON файла."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(valid_transactions, tmp)
            tmp_path = tmp.name
        yield tmp_path
        Path(tmp_path).unlink()

    def test_read_valid_json_file(self, temp_json_file, valid_transactions):
        """Тест чтения валидного JSON файла."""
        result = read_json_file(temp_json_file)
        assert result == valid_transactions
        assert len(result) == 3

    def test_read_empty_json_file(self):
        """Тест чтения пустого JSON файла."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            tmp.write("")
            tmp_path = tmp.name

        result = read_json_file(tmp_path)
        assert result == []

        Path(tmp_path).unlink()

    def test_read_invalid_json_file(self):
        """Тест чтения невалидного JSON файла."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            tmp.write("invalid json content")
            tmp_path = tmp.name

        result = read_json_file(tmp_path)
        assert result == []

        Path(tmp_path).unlink()

    def test_read_json_with_not_list(self):
        """Тест когда JSON содержит не список."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump({"id": 1, "name": "test"}, tmp)
            tmp_path = tmp.name

        result = read_json_file(tmp_path)
        assert result == []

        Path(tmp_path).unlink()

    def test_read_nonexistent_file(self):
        """Тест чтения несуществующего файла."""
        result = read_json_file("nonexistent_file.json")
        assert result == []

    def test_read_json_file_with_path_object(self, temp_json_file, valid_transactions):
        """Тест чтения с Path объектом."""
        path_obj = Path(temp_json_file)
        result = read_json_file(path_obj)
        assert result == valid_transactions
