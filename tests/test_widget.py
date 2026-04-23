import pytest

from src.widget import get_date, mask_account_card


@pytest.fixture
def valid_card_data() -> str:
    return "1234567890123456"


@pytest.fixture
def valid_account_data() -> str:
    return "1234567890"


@pytest.mark.parametrize(
    "input_data,expected_result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счёт 73654108430135874305", "Счёт **4305"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Сберкарта 9876543210987654", "Сберкарта 9876 54** **** 7654"),
        ("Карта 1111222233334444", "Карта 1111 22** **** 4444"),
    ],
)
def test_mask_account_card_valid(input_data: str, expected_result: str) -> None:
    """Тестирует маскирование карт и счетов с корректными данными."""
    result = mask_account_card(input_data)
    assert result == expected_result


@pytest.mark.parametrize(
    "invalid_input,expected_error",
    [
        ("", "Входная строка не может быть пустой"),
        ("   ", "Входная строка не может быть пустой"),
        ("Текст без номера", "Номер карты/счёта должен содержать только цифры"),
        ("Visa без номера", "Номер карты/счёта должен содержать только цифры"),
        ("Счёт без цифр", "Номер карты/счёта должен содержать только цифры"),
        ("Short 123", "Некорректная длина номера карты/счёта"),
    ],
)
def test_mask_account_card_invalid(invalid_input: str, expected_error: str) -> None:
    """Тестирует обработку некорректных входных данных."""
    with pytest.raises(ValueError, match=expected_error):
        mask_account_card(invalid_input)


@pytest.mark.parametrize(
    "input_date,expected_date",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-25T15:30:45.123456", "25.12.2023"),
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
    ],
)
def test_get_date(input_date: str, expected_date: str) -> None:
    """Тестирует преобразование даты из ISO формата в ДД.ММ.ГГГГ."""
    result = get_date(input_date)
    assert result == expected_date
