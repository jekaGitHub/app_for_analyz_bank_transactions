import json
import logging
import pandas as pd
import pytest
from _datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние 3 месяца, начиная от переданной даты.
    :param transactions: датафрейм с данными по операциям
    :param category: категория для отбора данных
    :param date: опциональная дата
    :return: датафрейм с операциями
    """
    if date is None:
        end_date = datetime.today()
    end_date = datetime.strptime(date, '%d.%m.%Y')

    start_date = datetime(end_date.day, end_date.month - 3, end_date.year)
    print(start_date)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"]).dt.date
    result_pd_by_date_and_category = transactions[(start_date <= transactions["Дата операции"] <= end_date) &
                                                  (transactions["Категория"] == category)]

    # logger.debug("Сформирован итоговый датафрейм с операциями")

    return result_pd_by_date_and_category
