"""
Модуль содержит абстрактный класс AbstractHtmlSupplier
для создания классов по предоставлению html страниц для парсинга.

И класс RequestsHtmlSupplier,
который использует библиотеку requests для предоставления html страниц.
"""

import logging
from time import sleep
from abc import ABC, abstractmethod

import requests
from fake_useragent import UserAgent

from logger_config import logger

SLEEP_SECONDS = 1
MAX_TIMEOUT = 1

logging.getLogger('urllib3').setLevel(logging.ERROR)


class AbstractHtmlSupplier(ABC):
    @abstractmethod
    def get(self, url: str, params=None) -> str:
        ...


class RequestsHtmlSupplier(AbstractHtmlSupplier):
    """
    Добавляет метод requests_get для получения HTML-страницы с использованием библиотеки requests.
    """

    def __init__(self):
        self.useragent = UserAgent()
        self.timeout = MAX_TIMEOUT

    def get(self, url: str, params=None) -> str:
        """
        Возвращает ответ на GET-запрос или пустую строку.

        :param url: URL-адрес.
        :param params: Дополнительные параметры.
        :return: HTML или пустую строку.
        """
        session = None
        headers = {'User-Agent': '', 'Accept': '*/*'}
        for i in range(3):  # три попытки получить страницу
            try:
                session = requests.Session()
                session.headers['User-Agent'] = self.useragent.random
                rq = session.get(url, params=params, headers=headers, timeout=self.timeout)
                if rq.status_code == 200:
                    sleep(SLEEP_SECONDS)
                    return rq.text
                else:
                    logger.info(f"{rq.status_code}: {url}")
                    sleep(SLEEP_SECONDS)
            except Exception as ex:
                logger.info(f"Функция RequestsMixin.requests_get вызвала исключение:\n{ex}")
            finally:
                session.close()
        return ''
