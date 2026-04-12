from src.masks import get_mask_account, get_mask_card_number

if __name__ == "__main__":
    card = "1234567890123456"
    account = "12345678901234567890"

    print(f"Маска карты: {get_mask_card_number(card)}")
    print(f"Маска счёта: {get_mask_account(account)}")
