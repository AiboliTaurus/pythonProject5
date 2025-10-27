import logging

from logging_config import setup_logger

# Настройка логера для модуля masks
logger = logging.getLogger(__name__)
if not logger.handlers:  # Защита от дублирования handler'ов
    logger = setup_logger("masks")


def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер карты по шаблону XXXX XX** **** XXXX
    :param card_number: номер карты в виде числа
    :return: замаскированный номер карты
    """
    card_str = str(card_number)

    if len(card_str) != 16:
        logger.error("Номер карты %s имеет длину %d (ожидается 16)", card_number, len(card_str))
        raise ValueError("Номер карты должен содержать 16 цифр")

    masked = card_str[:4] + " " + card_str[4:6] + "**" + " " + "****" + " " + card_str[-4:]
    logger.info("Номер карты %s успешно замаскирован как %s", card_number, masked)
    return masked


def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер счета по шаблону **XXXX
    :param account_number: номер счета в виде числа
    :return: замаскированный номер счета
    """
    account_str = str(account_number)

    if len(account_str) < 6:
        logger.error("Номер счета %s имеет длину %d (минимум 6)", account_number, len(account_str))
        raise ValueError("Номер счета должен содержать минимум 6 цифр")

    masked = "**" + account_str[-4:]
    logger.info("Номер счета %s успешно замаскирован как %s", account_number, masked)
    return masked
