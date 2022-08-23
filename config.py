import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from os import environ as env


DB_HOST = env.get('DB_HOST') or '127.0.0.1'
DB_PORT = env.get('DB_PORT') or 5584
DB_NAME = env.get('DB_NAME') or 'smart_transport'
DB_USER = env.get('DB_USER') or 'smart_transport'
DB_PWD = env.get('DB_PASS') or 'smart_transport'

CONTRACTOR_HOST = env.get('CONTRACTOR_HOST')
TOKEN = env.get('TOKEN')


def init_logger():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs('logs', exist_ok=True)
    console = logging.StreamHandler()
    file = RotatingFileHandler(
        'logs/{}.log'.format(datetime.now().strftime("%Y-%m-%d_%H-%M")),
        mode='a',
        maxBytes=1*1024*1024,
        backupCount=10,
        encoding='utf-8',
        delay=0
    )
    
    logging.basicConfig(
        handlers=(file, console),
        format='[%(asctime)s | %(levelname)s]: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO
    )
    
    logger = logging.getLogger()
    return logger


LOGGER = init_logger()
