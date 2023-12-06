import json
import logging
import os

logger = logging.getLogger(__name__)


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
                logger.error('Ошибка при преобразовании данных в JSON')
                return {}
    except FileNotFoundError:
        print(f'Файл {datafile} не найден.')
        logger.error('Файл не найден')
        return {}
    logger.info(f"Данные с настройками успешно получены из файла {os.getcwd()}\\{datafile}")
    return data
