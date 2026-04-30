import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def sample_card_data() -> dict[str, list[str]]:
    """Предоставляет тестовые данные для карт."""
    return {
        "valid": [
            "1234567890123456",
            "1234-5678-9012-3456",
            "1234 5678 9012 3456",
        ],
        "short": ["123456", "1", ""],
        "invalid": ["abc123", "12a45", "   "],
    }


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234-5678-9012-3456", "1234 56** **** 3456"),  # с дефисами
        ("1234 5678 9012 3456", "1234 56** **** 3456"),  # с пробелами
        ("123456789", "1234 56** **** 89"),  # 9 цифр → последние 2
        ("1234567890", "1234 56** **** 90"),  # 10 цифр → последние 2
        ("12345678901", "1234 56** **** 901"),  # 11 цифр → последние 3 (не 4!)
        ("123456789012", "1234 56** **** 012"),  # 12 цифр → последние 3
        ("1234567890123", "1234 56** **** 123"),  # 13 цифр → последние 3
        ("12345678901234", "1234 56** **** 234"),  # 14 цифр → последние 3
        ("123456789012345", "1234 56** **** 345"),  # 15 цифр → последние 3
        ("123456", "123456"),  # ровно 6 цифр
        ("1", "1"),  # очень короткий
        ("", ""),  # пустая строка
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210"),
        ("12", "12"),  # слишком короткий
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:

    result = get_mask_account("12345678901234567890")
    assert result == "**7890"
    assert get_mask_account(account_number) == expected

    # Дополнительные тесты
    assert get_mask_account("00000000000000000001") == "**0001"
    assert get_mask_account("9999") == "9999"  # короткий номер
    assert get_mask_account("1") == "1"  # очень короткий номер


@pytest.mark.parametrize("invalid_input", ["abc123", "12a45", "   "])
def test_get_mask_card_number_invalid(invalid_input: str) -> None:
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number(invalid_input)


def test_invalid_account_number() -> None:

    with pytest.raises(ValueError):
        get_mask_account("abc123")
