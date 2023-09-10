import logging
from time import sleep

from requests import get, Response
from fake_useragent import UserAgent

from logger_config import logger

SLEEP_SECONDS = 2
MAX_TIMEOUT = 1

logging.getLogger('urllib3').setLevel(logging.ERROR)


class RequestsMixin:
    """
    Добавляет метод requests_get для получения HTML-страницы с использованием библиотеки requests.
    """

    def __init__(self):
        self.useragent = UserAgent()

    def requests_get(self, url: str, params=None, timeout=MAX_TIMEOUT) -> Response | None:
        """
        Возвращает ответ на GET-запрос или пустую строку.

        :param url: URL-адрес.
        :param params: Дополнительные параметры.
        :param timeout: Максимальное время ожидания ответа.
        :return: :class:`Response <Response>` object или пустую строку.
        """
        headers = {'User-Agent': '', 'Accept': '*/*'}
        for i in range(3):  # три попытки получить страницу
            try:
                headers['User-Agent'] = self.useragent.random
                rq = get(url, params=params, headers=headers, timeout=timeout)
                if rq.status_code == 200:
                    return rq
                else:
                    logger.error(f"{rq.status_code}: {url}")
                    sleep(SLEEP_SECONDS)
            except Exception as ex:
                logger.error(f"Функция RequestsMixin.requests_get вызвала исключение:\n{ex}")
        return None
