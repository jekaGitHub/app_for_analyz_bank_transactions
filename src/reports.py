import logging
import os
from _datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "report.xlsx")


def report(*, filename: str = PATH_TO_FILE) -> Callable:
    """Функция записывает в файл результат, который возвращает декорируемая функция, формирующая отчет.
    :param filename: путь до файла, по умолчанию задан в константе
    :return: объект Callable
    """
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Optional[Any], **kwargs: Optional[Any]) -> Optional[Any]:
            try:
                result = func(*args, **kwargs)
                if filename.endswith(".xlsx"):
                    result.to_excel(filename, index=False)
                    logger.debug(f"Данные записаны в файл {filename}")
                else:
                    logger.error("Тип файла не поддерживается")
                    raise ValueError("Тип файла не поддерживается")
            except Exception as e:
                logger.error(f"Ошибка {e}")
                result = None
            return result
        return inner
    return wrapper


@report()
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
        end_date = datetime.now()
    end_date = datetime.strptime(date, '%d.%m.%Y')
    start_date = end_date + relativedelta(months=-3)

    start_date_new = pd.to_datetime(start_date, dayfirst=True)
    end_date_new = pd.to_datetime(end_date, dayfirst=True)

    print(start_date)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True). dt.date
    result_pd_by_date_and_category = transactions[(start_date_new <= transactions["Дата операции"] <= end_date_new) &
                                                  (transactions["Категория"] == category)]

    logger.info("Сформирован итоговый датафрейм с операциями")

    return result_pd_by_date_and_category
