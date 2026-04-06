import pytest
from src.widget import mask_account_card

def test_mask_account_card_card() -> None:
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"

def test_mask_account_card_account() -> None:
    result = mask_account_card("Счёт 73654108430135874305")
    assert result == "Счёт **4305"  # или другой ожидаемый формат

def test_mask_account_card_no_number() -> None:
    result = mask_account_card("Текст без номера")
    assert result == "Текст без номера"