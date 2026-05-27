"""Главный модуль программы для работы с банковскими транзакциями."""

import os
from pathlib import Path

from src.file_reader import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date, filter_by_currency, filter_by_description
from src.search_utils import search_transactions
from src.utils import read_json_file
from src.widget import mask_account_card, get_date


def load_transactions(file_type: str) -> list:
    """
    Загружает транзакции из выбранного файла.

    Args:
        file_type: Тип файла (1 - JSON, 2 - CSV, 3 - Excel)

    Returns:
        Список транзакций
    """
    data_dir = Path("data")

    if file_type == "1":
        print("Для обработки выбран JSON-файл.")
        return read_json_file(data_dir / "operations.json")
    elif file_type == "2":
        print("Для обработки выбран CSV-файл.")
        return read_csv_file(data_dir / "transactions.csv")
    elif file_type == "3":
        print("Для обработки выбран XLSX-файл.")
        return read_excel_file(data_dir / "transactions_excel.xlsx")
    else:
        print("Неверный выбор. Попробуйте снова.")
        return None


def get_valid_status() -> str:
    """
    Запрашивает у пользователя статус транзакций с проверкой корректности.

    Returns:
        Корректный статус
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        status = input().upper()

        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        else:
            print(f"Статус операции \"{status}\" недоступен.")


def get_yes_no(prompt: str) -> bool:
    """
    Запрашивает ответ Да/Нет.

    Args:
        prompt: Текст приглашения

    Returns:
        True если Да, False если Нет
    """
    while True:
        answer = input(prompt).lower()
        if answer in ["да", "yes", "y", "д"]:
            return True
        elif answer in ["нет", "no", "n", "н"]:
            return False
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def print_transactions(transactions: list) -> None:
    """
    Выводит список транзакций в отформатированном виде.

    Args:
        transactions: Список транзакций
    """
    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "Без описания")

        # Маскируем отправителя и получателя
        from_info = transaction.get("from", "")
        to_info = transaction.get("to", "")

        from_masked = mask_account_card(from_info) if from_info else "Неизвестно"
        to_masked = mask_account_card(to_info) if to_info else "Неизвестно"

        # Получаем сумму и валюту
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("code", "руб.")

        print(f"{date} {description}")
        print(f"{from_masked} -> {to_masked}")
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор источника данных
    while True:
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input().strip()
        transactions = load_transactions(choice)

        if transactions is not None:
            break

    if not transactions:
        print("Не удалось загрузить транзакции. Программа завершает работу.")
        return

    # Фильтрация по статусу
    status = get_valid_status()
    filtered_transactions = filter_by_state(transactions, status)

    if not filtered_transactions:
        print("Не найдено транзакций с выбранным статусом.")
        return

    # Сортировка по дате
    if get_yes_no("\nОтсортировать операции по дате? Да/Нет\n"):
        order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        reverse = order == "по убыванию" or order == "убыванию" or order == "desc"
        filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

    # Фильтрация по рублевым транзакциям
    if get_yes_no("\nВыводить только рублевые транзакции? Да/Нет\n"):
        filtered_transactions = filter_by_currency(filtered_transactions, "RUB")

    # Поиск по описанию
    if get_yes_no("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            filtered_transactions = search_transactions(filtered_transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":
    main()