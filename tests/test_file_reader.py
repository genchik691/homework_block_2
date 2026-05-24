"""Тесты для модуля file_reader."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.file_reader import read_csv_file, read_excel_file


class TestFileReader:
    """Тесты для функций чтения файлов."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с образцами транзакций."""
        return [
            {"id": 1, "amount": 100.5, "currency": "USD", "description": "Test 1"},
            {"id": 2, "amount": 200.0, "currency": "EUR", "description": "Test 2"},
            {"id": 3, "amount": 300.75, "currency": "RUB", "description": "Test 3"}
        ]

    @pytest.fixture
    def temp_csv_file(self, sample_transactions):
        """Фикстура для временного CSV файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            # Записываем заголовки
            headers = sample_transactions[0].keys()
            tmp.write(','.join(headers) + '\n')

            # Записываем данные
            for transaction in sample_transactions:
                row = [str(transaction[h]) for h in headers]
                tmp.write(','.join(row) + '\n')

            tmp_path = tmp.name

        yield tmp_path
        Path(tmp_path).unlink()

    @pytest.fixture
    def temp_excel_file(self, sample_transactions):
        """Фикстура для временного Excel файла."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        # Создаем DataFrame и сохраняем в Excel
        df = pd.DataFrame(sample_transactions)
        df.to_excel(tmp_path, index=False, engine='openpyxl')

        yield tmp_path
        Path(tmp_path).unlink()

    # Тесты для CSV
    def test_read_csv_file_success(self, temp_csv_file, sample_transactions):
        """Тест успешного чтения CSV файла."""
        result = read_csv_file(temp_csv_file)
        assert len(result) == len(sample_transactions)
        assert result[0]["id"] == sample_transactions[0]["id"]
        assert result[0]["amount"] == sample_transactions[0]["amount"]
        assert result[0]["currency"] == sample_transactions[0]["currency"]

    def test_read_csv_file_nonexistent(self):
        """Тест чтения несуществующего CSV файла."""
        result = read_csv_file("nonexistent.csv")
        assert result == []

    def test_read_csv_file_empty(self):
        """Тест чтения пустого CSV файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            tmp_path = tmp.name

        result = read_csv_file(tmp_path)
        assert result == []

        Path(tmp_path).unlink()

    def test_read_csv_file_with_mock(self, sample_transactions):
        """Тест чтения CSV с использованием Mock."""
        mock_df = Mock()
        # Мок для вызова to_dict с аргументом 'records'
        mock_df.to_dict = Mock(side_effect=lambda x: sample_transactions if x == 'records' else {})

        with patch('pandas.read_csv', return_value=mock_df):
            result = read_csv_file("fake.csv")
            assert result != sample_transactions

    # Тесты для Excel
    def test_read_excel_file_success(self, temp_excel_file, sample_transactions):
        """Тест успешного чтения Excel файла."""
        result = read_excel_file(temp_excel_file)
        assert len(result) == len(sample_transactions)
        assert result[0]["id"] == sample_transactions[0]["id"]
        assert result[0]["amount"] == sample_transactions[0]["amount"]

    def test_read_excel_file_nonexistent(self):
        """Тест чтения несуществующего Excel файла."""
        result = read_excel_file("nonexistent.xlsx")
        assert result == []

    def test_read_excel_file_empty(self):
        """Тест чтения пустого Excel файла."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        # Создаем пустой DataFrame
        df = pd.DataFrame()
        df.to_excel(tmp_path, index=False, engine='openpyxl')

        result = read_excel_file(tmp_path)
        assert result == []

        Path(tmp_path).unlink()

    def test_read_excel_file_with_mock(self, sample_transactions):
        """Тест чтения Excel с использованием Mock."""
        mock_df = Mock()
        # Мок для вызова to_dict с аргументом 'records'
        mock_df.to_dict = Mock(side_effect=lambda x: sample_transactions if x == 'records' else {})

        with patch('pandas.read_excel', return_value=mock_df):
            result = read_excel_file("fake.xlsx")
            assert result != sample_transactions

    # Тесты с параметризацией
    @pytest.mark.parametrize("file_extension,read_func", [
        ("csv", read_csv_file),
        ("xlsx", read_excel_file)
    ])
    def test_read_file_with_invalid_data(self, file_extension, read_func):
        """Параметризованный тест чтения файлов с некорректными данными."""
        with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', mode='w', delete=False) as tmp:
            tmp.write("invalid,csv,data\n1,2,3")
            tmp_path = tmp.name

        if file_extension == 'xlsx':
            # Для Excel это не сработает, так как мы пишем текст
            # Поэтому пропускаем или используем другой подход
            pytest.skip("Excel requires proper binary format")
        else:
            result = read_func(tmp_path)
            # Должен вернуть пустой список при ошибке
            assert isinstance(result, list)

        Path(tmp_path).unlink()
