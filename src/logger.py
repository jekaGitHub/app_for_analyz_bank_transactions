import logging


def setup_logging() -> logging.Logger:
    """Конфигуратор логгера"""
    logging.basicConfig(filename='../data/log_file.log', filemode="w+", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger()
