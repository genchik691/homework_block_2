def test_get_mask_card_number() -> None:
    from src.masks import get_mask_card_number

    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"

    # Дополнительные тесты
    assert get_mask_card_number("0000111122223333") == "0000 11** **** 3333"
    assert get_mask_card_number("9876543210987654") == "9876 54** **** 7654"


def test_get_mask_account() -> None:
    from src.masks import get_mask_account

    result = get_mask_account("12345678901234567890")
    assert result == "**7890"

    # Дополнительные тесты
    assert get_mask_account("00000000000000000001") == "**0001"
    assert get_mask_account("9999") == "9999"  # короткий номер
    assert get_mask_account("1") == "1"  # очень короткий номер


def test_invalid_card_number() -> None:
    import pytest

    from src.masks import get_mask_card_number

    with pytest.raises(ValueError):
        get_mask_card_number("12345")  # слишком короткий

    with pytest.raises(ValueError):
        get_mask_card_number("abc123")  # не цифры


def test_invalid_account_number() -> None:
    import pytest

    from src.masks import get_mask_account

    with pytest.raises(ValueError):
        get_mask_account("abc123")
