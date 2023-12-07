import json
import logging

logger = logging.getLogger(__name__)

BY_SEARCH_FILE = 'list_search.json'


def get_operations_by_find_str_put_json(data: list[dict], search_str: str) -> json:
    """
    Функция принимает на вход строку поиска, возвращается json-ответ со всеми транзакциями, содержащими запрос
    в описании или категории.
    :param data: список словарей
    :param search_str: строка поиска
    """
    results = [item for item in data if search_str.strip() in (item["Описание"], item["Категория"])]

    with open(BY_SEARCH_FILE, 'w', encoding='utf-8') as f:
        # json.dump(results, f, ensure_ascii=False, indent=4)
        json_response = json.dumps(results, ensure_ascii=False, indent=4)

        logger.info("Данные записаны в файл")
    return json_response
