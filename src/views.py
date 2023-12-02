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
    return pd.read_excel(filename)


def get_currency_rate(base: str) -> float:
    """Получает курс от API и возвращает его в виде float"""
    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    return rate


def get_stock_rate(base: str) -> float:
    """Получает курс акций от API и возвращает его в виде float"""
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=symbol&apikey=apikey'
    # url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE'

    response = requests.get(url, params={'symbol': base}, headers={'apikey': STOCK_API_KEY})
    data = response.json()['Global Quote']['05. price']
    return data


if __name__ == '__main__':
    # print(get_currency_rate('EUR'))

    # filename = "../data/operations.xls"
    # xls_file = get_operations_from_xls("../data/operations.xls")
    # print(xls_file)
    # print(xls_file.loc[0, "Сумма операции"])
    # print(xls_file.head())
    # print(xls_file.shape)
    print(get_stock_rate("AAPL"))


