import os

from src.views import (get_operations_from_xls, get_list_operations_from_dataframe, get_operations_by_date,
                       get_result_list_dictionaries)
from src.services import get_operations_by_find_str_put_json
from src.reports import spending_by_category
from logger import setup_logging

FILE_OPERATIONS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xls')

logger = setup_logging()


def main():
    logger.info("Начало программы....")

    # получаем данные из файла эксель в формате датафрейм
    df = get_operations_from_xls(FILE_OPERATIONS)

    # преобразовываем датафрейм в список словарей
    operations = get_list_operations_from_dataframe(df)

    # получаем операции за определённый период
    transactions = get_operations_by_date(operations, "2021-12-02 21:45:00")

    # получаем json-ответ с запрашиваемыми данными
    print(get_result_list_dictionaries(transactions))

    # получаем данные по строке поиска в описании или категории и записываем их в файл
    get_operations_by_find_str_put_json(operations, "Госуслуги")

    # получаем траты по заданной категории за последние 3 месяца и отправляем отчет в файл report.xlsx
    print(spending_by_category(df, "Госуслуги", "24.12.2021"))

    logger.info("Финиш программы")


if __name__ == '__main__':
    main()
