import json
import logging
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from utils import get_list_user_settings_from_json

logger = logging.getLogger(__name__)


def greetings() -> str:
    """
    Функция возвращает строку приветствия.
    :return: возвращает данные в строковом формате
    """
    time_now = datetime.now()

    if 6 <= time_now.hour < 12:
        greeting = 'Доброе утро!'
    elif 12 <= time_now.hour < 18:
        greeting = 'Доброе день!'
    elif 18 <= time_now.hour < 23:
        greeting = 'Доброе вечер!'
    else:
        greeting = 'Доброй ночи!'

    logger.info('Создано приветствие')

    return greeting


def get_operations_from_xls(filename: str) -> Any:
    """
    Функция принимает путь до файла загрузки и возвращает датафрейм с данными.
    :param filename: путь до файла загрузки
    :return: датафрейм
    """
    logger.debug('Происходит загрузка данных из файла формата .xls')

    df = pd.read_excel(filename)

    logger.info('Данные успешно получены')

    return df


def get_list_operations_from_dataframe(data: pd.DataFrame) -> list[dict]:
    """
    Функция принимает датафрейм и преобразует его в список словарей.
    :param data: датафрейм
    :return: список словарей с операциями
    """

    dict_operations = data.to_dict(orient='records')

    logger.info('Сформирован список словарей из датафрейма.')

    return dict_operations


def get_operations_by_date(data: list[dict], date_operations: str) -> list[dict]:
    """
    Функция возвращает список словарей с данными о финансовых транзакциях за период.
    :param data: список словарей с операциями
    :param date_operations: конечная дата периода
    :return: список словарей за период от начала месяца до введенной даты
    """

    logger.debug('Происходит преобразование дат в datetime и рассчитывается начальная дата')

    format_: str = '%Y-%m-%d %H:%M:%S'
    end_date = datetime.strptime(date_operations, format_)
    start_date = datetime(end_date.year, end_date.month, 1, 0, 0, 0)

    transactions = [item for item in data if start_date <= datetime.strptime(item["Дата операции"],
                                                                             '%d.%m.%Y %H:%M:%S') <= end_date
                    and item["Статус"] == 'OK']
    logger.info('Данные успешно получены')
    return transactions


def get_operations_to_card(transactions: list[dict]) -> list[dict]:
    """
    Функция показывает информацию по каждой карте: последние 4 цифры карты, общую сумму расходов, кэшбэк.
    :param transactions: список словарей с операциями отобранные за определённый период
    :return: возвращает список словарей в заданном формате
    """
    operations_to_card = []

    logger.debug('Получение информации по карте')

    list_cards: set = set([item["Номер карты"] for item in transactions])

    for card in list_cards:
        total_spent = 0
        cashback = 0
        for transaction in transactions:
            if transaction["Номер карты"] == card:
                total_spent += abs(round(transaction["Сумма операции"], 2))
                cashback += round(abs(transaction["Сумма операции"]) / 100, 2)

        dict_operations = {
            'last_digits': str(card)[-4:],
            'total_spent': total_spent,
            'cashback': cashback
        }
        operations_to_card.append(dict_operations)

    logger.info('Данные по карте успешно получены')

    return operations_to_card


def get_list_dictionaries_sorted_by_sum(data: list[dict], sort_order: bool = True) -> list[dict]:
    """
    Функция возвращает топ-5 транзакций по сумме платежа. Необязательный аргумент задает порядок сортировки
    (убывание, возрастание).
    :param data: список словарей отобранных за период
    :param sort_order: порядок сортировки, по умолчанию = True, на убывание
    :return: список словарей в заданном формате
    """
    sorted_dictionaries = sorted(data, key=lambda data_dict: abs(data_dict["Сумма платежа"]), reverse=sort_order)[:5]
    top_transactions = []
    for item in sorted_dictionaries:
        dict_top_transactions = {
            'date': item["Дата платежа"],
            'amount': round(item["Сумма платежа"], 2),
            'category': item["Категория"],
            'description': item["Описание"]
        }
        top_transactions.append(dict_top_transactions)

    logger.info('Топ-5 транзакций по сумме платежа успешно получены')

    return top_transactions


def get_currency_rate(base: str) -> float:
    """Получает курс от API и возвращает его в виде float."""
    load_dotenv()

    api_key: str = os.getenv('RATE_API_KEY')

    if api_key is None:
        logger.error('Ключ API отсутствует!')
        raise ValueError('Ключ API отсутствует!')
    try:
        url = "https://api.apilayer.com/exchangerates_data/latest"

        response = requests.get(url, headers={'apikey': api_key}, params={'base': base})
        rate = response.json()['rates']['RUB']

        logger.info('Получен курс валюты!')

        return round(float(rate), 2)
    except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
        logger.error(f"Возникла ошибка {e}")
        raise ValueError("Что-то пошло не так!")


def get_stock_rate(base: str) -> float:
    """Получает курс акций от API и возвращает его в виде str."""
    load_dotenv()

    stock_api_key: str = os.getenv('STOCK_API_KEY')

    if stock_api_key is None:
        logger.error('Ключ API отсутствует!')
        raise ValueError('Ключ API отсутствует!')
    try:
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=symbol&apikey=apikey'

        response = requests.get(url, params={'symbol': base}, headers={'apikey': stock_api_key})
        data = response.json()['Global Quote']['05. price']

        logger.info('Получен курс акции!')

        return float(data)
    except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
        logger.error(f"Возникла ошибка {e}")
        raise ValueError("Что-то пошло не так!")


def get_list_stocks_rates() -> list[dict]:
    """
    Функция возвращает список словарей по стоимости акций в заданном формате.
    """
    list_stock = get_list_user_settings_from_json("../user_settings.json")['user_stocks']

    stock_prices = []

    for stock in list_stock:
        dict_stocks = {
            'stock': stock,
            'price': get_stock_rate(stock)
        }
        stock_prices.append(dict_stocks)

    logger.info('Список с курсами акций сформирован!')

    return stock_prices


def get_list_currency_rates() -> list[dict]:
    """
    Функция возвращает список словарей по стоимости валют в заданном формате.
    """
    list_currency = get_list_user_settings_from_json("../user_settings.json")['user_currencies']

    currency_rates = []

    for rate in list_currency:
        dict_rates = {
            'currency': rate,
            'rate': get_currency_rate(rate)
        }
        currency_rates.append(dict_rates)

    logger.info('Список с курсами валют сформирован!')

    return currency_rates


def get_result_list_dictionaries(transactions: list[dict]) -> json:
    result_dict = {
        'greeting': greetings(),
        'cards': get_operations_to_card(transactions),
        'top_transactions': get_list_dictionaries_sorted_by_sum(transactions),
        'currency_rates': get_list_currency_rates(),
        'stock_prices': get_list_stocks_rates()
    }
    json_answer = json.dumps(result_dict, ensure_ascii=False, indent=4)

    logger.info('JSON ответ сформирован!')

    return json_answer
