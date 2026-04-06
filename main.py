from src.masks import get_mask_card_number, get_mask_account

if __name__ == "__main__":
    card = "1234567890123456"
    account = "1234567890"

    print(f"Маска карты: {get_mask_card_number(card)}")
    print(f"Маска счёта: {get_mask_account(account)}")
