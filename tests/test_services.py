import json

from src.services import get_operations_by_find_str_put_json
from tests.test_reports import test_list


def test_get_operations_by_find_str_put_json(test_list):
    result = json.loads(get_operations_by_find_str_put_json(test_list, "Кафе"))
    assert result == [{'Дата операции': '25.10.2023 12:25:05',
                       'Номер карты': "*6780",
                       'Статус': 'OK',
                       'Сумма операции': -2299.99,
                       'Валюта операции': "RUB",
                       'Кэшбэк': 5.0,
                       'Категория': 'Кафе',
                       'Описание': 'Такси'
                       }]
