import logging
import os

from config.settings import PROJECT_NAME


def get_pipeline_logger(log_name: str):
    path = '/mnt/data/log/{}/word_pipeline'.format(PROJECT_NAME)
    if not os.path.exists(path):
        os.makedirs(path)
    return get_logger(log_name, path)


def get_worker_logger(log_name: str):
    path = '/mnt/data/log/{}/word_worker'.format(PROJECT_NAME)
    if not os.path.exists(path):
        os.makedirs(path)
    return get_logger(log_name, path)


def get_global_logger():
    path = '/mnt/data/log/{}'.format(PROJECT_NAME)
    if not os.path.exists(path):
        os.makedirs(path)

    return get_logger(PROJECT_NAME, path)


def get_logger(log_name: str, path: str):
    FORMAT = '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', handlers=[
        logging.FileHandler(
            filename="{0}/{1}.log".format(path, log_name),
            encoding='utf8'
        ),
        logging.StreamHandler()
    ])
    logger = logging.getLogger(log_name)
    return logger
