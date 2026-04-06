import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card_card() -> None:
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"


def test_mask_account_card_account() -> None:
    result = mask_account_card("Счет 73654108430135874305")
    assert result == "Счет **4305"


def test_mask_account_card_no_number() -> None:
    with pytest.raises(ValueError):
        mask_account_card("Текст без номера")


def test_get_date() -> None:
    result = get_date("2024-03-11T02:26:18.671407")
    assert result == "11.03.2024"
