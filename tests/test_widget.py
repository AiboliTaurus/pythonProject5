import pytest
from src.widget import mask_account_card


# Обновленные тесты с использованием фикстур
def test_mask_account_card_card(card_test_data):
    input_text, expected_result = card_test_data
    result = mask_account_card(input_text)
    assert result == expected_result

def test_mask_account_card_account(account_test_data):
    input_text, expected_result = account_test_data
    result = mask_account_card(input_text)
    assert result == expected_result

def test_mask_account_card_invalid(invalid_input):
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)