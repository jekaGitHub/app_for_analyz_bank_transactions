import json
from datetime import datetime
from unittest.mock import patch
import pandas as pd

import pytest
import requests
from src.views import greetings, get_operations_from_xls, get_list_operations_from_dataframe, get_list_stocks_rates


@pytest.mark.parametrize("data, expected_result", [
    (datetime(2023, 12, 7, 6, 5, 30), "Доброе утро!"),
    (datetime(2023, 12, 7, 16, 16, 16), "Добрый день!"),
    (datetime(2023, 12, 7, 18, 35, 30), "Добрый вечер!"),
    (datetime(2023, 12, 7, 00, 15, 15), "Доброй ночи!")
])
@patch("src.views.datetime")
def test_greetings(mock_datetime, data, expected_result):
    mock_datetime.now.return_value = data
    assert greetings() == expected_result


@patch("src.views.pd.read_excel")
def test_get_operations_from_xls(mock_read_excel, dataframe):
    mock_read_excel.return_value = dataframe
    result = get_operations_from_xls("mock.xls")
    assert result.equals(dataframe)


def test_get_list_operations_from_dataframe(dataframe):
    assert get_list_operations_from_dataframe(dataframe) == [
        {
            "date": "01.12.2021",
            "amount": -199.0,
            "category": "Дом и ремонт",
            "description": "Строитель"
        },
        {
            "date": "02.12.2021",
            "amount": -125.0,
            "category": "Фастфуд",
            "description": "ЦЕХ 85"
        },
        {
            "date": "01.12.2021",
            "amount": -99.22,
            "category": "Супермаркеты",
            "description": "Дикси"
        }
    ]


def test_get_list_stocks_rates(stocks):
    assert get_list_stocks_rates(stocks) == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
