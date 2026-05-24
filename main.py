"""Главный модуль для демонстрации работы логирования."""

from pathlib import Path
from src.masks import get_mask_card_number, get_mask_account
from src.utils import read_json_file


def main():
    """Демонстрация работы функций с логированием."""
    print("=" * 50)
    print("Демонстрация работы логирования")
    print("=" * 50)

    # 1. Тестирование маскирования карт и счетов
    print("\n1. Тестирование masks.py:")
    try:
        card_number = "7000792289606361"
        masked_card = get_mask_card_number(card_number)
        print(f"  Карта: {card_number} -> {masked_card}")
    except Exception as e:
        print(f"  Ошибка: {e}")

    try:
        account_number = "73654108430135874305"
        masked_account = get_mask_account(account_number)
        print(f"  Счет: {account_number} -> {masked_account}")
    except Exception as e:
        print(f"  Ошибка: {e}")

    # 2. Тестирование чтения JSON файла
    print("\n2. Тестирование utils.py:")

    # Успешный случай
    try:
        transactions = read_json_file("data/operations.json")
        print(f"  Успешно загружено {len(transactions)} транзакций")
    except Exception as e:
        print(f"  Ошибка: {e}")

    # Ошибочный случай - файл не существует
    print("\n  Попытка загрузить несуществующий файл:")
    transactions = read_json_file("data/nonexistent.json")
    print(f"  Результат: загружено {len(transactions)} транзакций")

    # Ошибочный случай - пустой файл
    print("\n  Попытка загрузить пустой файл (создаем временный):")
    try:
        empty_file = Path("data/empty.json")
        empty_file.touch()  # Создаем пустой файл
        transactions = read_json_file(empty_file)
        print(f"  Результат: загружено {len(transactions)} транзакций")
        empty_file.unlink()  # Удаляем временный файл
    except Exception as e:
        print(f"  Ошибка: {e}")

    print("\n" + "=" * 50)
    print("Логи записаны в папку logs/")
    print("- masks.log - логи маскирования")
    print("- utils.log - логи работы с JSON")
    print("=" * 50)


if __name__ == "__main__":
    main()