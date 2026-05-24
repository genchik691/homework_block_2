"""Главный модуль для демонстрации работы логирования и чтения файлов."""

from pathlib import Path
from src.masks import get_mask_card_number, get_mask_account
from src.utils import read_json_file
from src.file_reader import read_csv_file, read_excel_file


def main():
    """Демонстрация работы функций."""
    print("=" * 50)
    print("Демонстрация работы с файлами")
    print("=" * 50)

    # 1. Чтение JSON файла
    print("\n1. Чтение JSON файла:")
    json_transactions = read_json_file("data/operations.json")
    print(f"  Загружено {len(json_transactions)} транзакций из JSON")

    # 2. Чтение CSV файла
    print("\n2. Чтение CSV файла:")
    csv_transactions = read_csv_file("data/transactions.csv")
    print(f"  Загружено {len(csv_transactions)} транзакций из CSV")
    if csv_transactions:
        print(f"  Пример: {csv_transactions[0]}")

    # 3. Чтение Excel файла
    print("\n3. Чтение Excel файла:")
    excel_transactions = read_excel_file("data/transactions_excel.xlsx")
    print(f"  Загружено {len(excel_transactions)} транзакций из Excel")
    if excel_transactions:
        print(f"  Пример: {excel_transactions[0]}")

    print("\n" + "=" * 50)
    print("Логи записаны в папку logs/")
    print("- file_reading.log - логи чтения CSV/Excel")
    print("=" * 50)


if __name__ == "__main__":
    main()