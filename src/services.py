import json
import logging
import pytest
from views import get_operations_from_xls


BY_SEARCH_FILE = 'list_search.json'


def get_operations_by_find_str_put_json(search_str: str) -> None:
    """
    Функция принимает на вход строку поиска, и выводит список транзакций, содержащими запрос в описании или категории.
    :param search_str: строка поиска
    :return: список транзакций, удовлетворяющий условиям
    """
    data = get_operations_from_xls("../data/operations.xls")

    results = [item for item in data if search_str.strip() in (item["Описание"], item["Категория"])]

    with open(BY_SEARCH_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    print(get_operations_by_find_str_put_json("Госуслуги"))
