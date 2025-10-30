def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер карты по шаблону XXXX XX** **** XXXX

    :param card_number: номер карты в виде числа
    :return: замаскированный номер карты
    """
    # Преобразуем число в строку
    card_str = str(card_number)

    # Проверяем корректность длины номера карты
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Формируем маску
    masked = (
        card_str[:4]
        + " "  # первые 4 цифры
        + card_str[4:6]
        + "**"
        + " "  # следующие 2 цифры и **
        + "****"
        + " "  # четыре звездочки
        + card_str[-4:]  # последние 4 цифры
    )

    return masked


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер счета по шаблону **XXXX

    :param account_number: номер счета в виде числа
    :return: замаскированный номер счета
    """
    # Преобразуем число в строку
    account_str = str(account_number)

    # Проверяем минимальную длину номера счета
    if len(account_str) < 6:
        raise ValueError("Номер счета должен содержать минимум 6 цифр")

    # Формируем маску
    masked = "**" + account_str[-4:]

    return masked
