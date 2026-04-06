from src.widget import mask_account_card, get_date



def test_mask_account_card_card() -> None:
    result = mask_account_card("Visa Platinum 7000792289606361")
    assert result == "Visa Platinum 7000 79** **** 6361"


    result = mask_account_card("Maestro 1596837868705199")
    assert result == "Maestro 1596 83** **** 5199"

    result = mask_account_card("MasterCard 7158300734726758")
    assert result == "MasterCard 7158 30** **** 6758"



def test_mask_account_card_account() -> None:
    result = mask_account_card("Счёт 73654108430135874305")
    assert result == "Счёт **4305"

    result = mask_account_card("Счёт 64686473678894779589")
    assert result == "Счёт **9589"




def test_get_date() -> None:
    result = get_date("2024-03-11T02:26:18.671407")
    assert result == "11.03.2024"

    result = get_date("2023-12-25T15:30:45.123456")
    assert result == "25.12.2023"