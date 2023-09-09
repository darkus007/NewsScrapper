"""
Модуль инициализации логера (logging.Logger).
"""

import logging.handlers
from sys import stdout

LOGGER_LEVEL = "DEBUG"


logger = logging.getLogger("spyder")
logger.setLevel(LOGGER_LEVEL)

log_format = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S ')

file_handler = logging.handlers.RotatingFileHandler(filename=f'logs/{__name__}.log',
                                                    mode='a',
                                                    maxBytes=1048576,   # 1 Мегабайт = 1048576 Байт
                                                    backupCount=10)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(log_format)

stream_handler = logging.StreamHandler(stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(log_format)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
