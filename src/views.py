import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv('RATE_API_KEY')
STOCK_API_KEY: str = os.getenv('STOCK_API_KEY')


def greetings() -> str:
    time_now = datetime.now()

    if 6 <= time_now.hour < 12:
        greeting = 'Доброе утро!'
    elif 12 <= time_now.hour < 18:
        greeting = 'Доброе день!'
    elif 18 <= time_now.hour < 23:
        greeting = 'Доброе вечер!'
    else:
        greeting = 'Доброй ночи!'
    return greeting


def get_operations_from_xls(filename: str):
    df = pd.read_excel(filename)
    return df


def get_operations_by_date():
    date_now = datetime.now()
    # month = date_now.month
    start_date = datetime(date_now.year, date_now.month, 1, 0, 0, 0)
    new_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%Y %H:%M:%S.%f')
    return new_date


def get_list_user_settings_from_json(datafile: str) -> dict:
    """Принимает на вход путь до JSON-файла и возвращает словарь с пользовательскими настройками.

    :param datafile: путь к файлу json
    :return: dict, который содержит пользовательские настройки
    """
    try:
        with open(datafile, encoding='utf-8') as f:
            try:
                data: dict = json.load(f)
            except json.JSONDecodeError:
                print('Ошибка при преобразовании в JSON данных из файла.')
                # logger.error('Ошибка при преобразовании данных в JSON')
                return {}
    except FileNotFoundError:
        print(f'Файл {datafile} не найден.')
        # logger.error('Файл не найден')
        return {}
    # logger.info(f"Данные о финансовых транзакциях успешно получены из файла {os.getcwd()}\\{datafile}")
    return data


def get_currency_rate(base: str) -> float:
    """Получает курс от API и возвращает его в виде float"""
    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    return round(float(rate), 2)


def get_stock_rate(base: str) -> float:
    """Получает курс акций от API и возвращает его в виде str"""
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=symbol&apikey=apikey'
    # url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE'

    response = requests.get(url, params={'symbol': base}, headers={'apikey': STOCK_API_KEY})
    data = response.json()['Global Quote']['05. price']
    return float(data)


def get_list_stocks_rates() -> list:
    list_stock = get_list_user_settings_from_json("../user_settings.json")['user_stocks']

    stock_prices = []

    for stock in list_stock:
        dict_stocks = {
            'stock': stock,
            'price': get_stock_rate(stock)
        }
        stock_prices.append(dict_stocks)
    return stock_prices


def get_list_currency_rates() -> list:
    list_currency = get_list_user_settings_from_json("../user_settings.json")['user_currencies']

    currency_rates = []

    for rate in list_currency:
        dict_rates = {
            'currency': rate,
            'rate': get_currency_rate(rate)
        }
        currency_rates.append(dict_rates)
    return currency_rates


if __name__ == '__main__':
    # print(get_currency_rate('EUR'))

    # filename = "../data/operations.xls"
    # xls_file = get_operations_from_xls("../data/operations.xls")
    # print(xls_file)
    # print(xls_file.loc[0, "Сумма операции"])
    # print(xls_file.head())
    # print(xls_file.shape)
    # print(get_stock_rate("AAPL"))

    # print(get_list_user_settings_from_json("../user_settings.json"))
    # print(get_list_stocks_rates())
    # print(get_list_currency_rates())
    # print(get_operations_from_xls("../data/operations.xls"))
    print(get_operations_by_date())
