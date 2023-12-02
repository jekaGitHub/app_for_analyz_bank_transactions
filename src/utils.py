import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv('RATE_API_KEY')


def greetings() -> str:
    time_now = datetime.now()

    if 5 <= time_now.hour < 11:
        greeting = 'Доброе утро!'
    elif 11 <= time_now.hour < 17:
        greeting = 'Доброе день!'
    elif 17 <= time_now.hour < 23:
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


if __name__ == '__main__':
    # print(get_currency_rate('EUR'))

    filename = "../data/operations.xls"
    xls_file = get_operations_from_xls("../data/operations.xls")
    print(xls_file)
    # print(xls_file.loc[0, "Сумма операции"])
    # print(xls_file.head())
    # print(xls_file.shape)
