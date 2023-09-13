#!/usr/bin/env python3
"""
Модуль содержит класс Spyder
который обходит произвольный сайт с глубиной до 2 и сохраняет html, url и title страницы в хранилище;
отображает собранные данные.

CLI (command line interface):
    * По урлу сайта и глубине обхода загружаются данные.
    * По урлу сайта из хранилища можно получить n прогруженных страниц (url и title).

Пример:
spider.py load http://www.vesti.ru --depth 1 -f -s
>> ok, execution time: 10s, peak memory usage: 100 Mb
    где:
    --depth 1 - глубина обхода страниц (0 - только главная страница, 1 - главная страница и все ссылки с нее, ...);
    -f - фильтровать по доменному имени сайта (в примере vesti);
    -s - динамически отображает собранные данные (необязательный параметр).

spider.py get http://www.vesti.ru -n 10
>> http://www.vesti.ru/news/: "Вести.Ru: новости, видео и фото дня"
>> http://www.vestifinance.ru/: "Вести Экономика: Главные события российской и мировой экономики, деловые новости,
фондовый рынок"
>> ...
    где:
    -n - количество выводимой информации (в примере 10 записей).
"""
import sys
import tracemalloc
from typing import Type

from utilites import resource_monitor, get_args
from scrapper import AbstractScrapper, Scrapper
from database import AbstractRepository, PostgreSQL
from logger_config import logger


class ScrapperNotPresented(Exception):
    pass


class RepositoryNotPresented(Exception):
    pass


class Spider:
    """
    Обходит произвольный сайт с глубиной до 2
    и сохраняет html, url и title страницы в хранилище.
    Отображает в терминале дынные из хранилища.
    """

    def __init__(self, url: str) -> None:
        self.url = url if url[-1] == '/' else url + "/"
        self._scrapper: Type[AbstractScrapper] | None = None
        self._database: Type[AbstractRepository] | None = None
        self.display_info: bool = False

    @resource_monitor
    def load(self, depth: int = 0, filtered: bool = True) -> None:
        """
        Загружает данные в хранилище.
        :param depth: глубина обхода.
        :param filtered: фильтрация по домену.
        """
        if self._scrapper is None:
            raise ScrapperNotPresented("Не предоставлен скраппер.")
        if self._database is None:
            raise RepositoryNotPresented("Не предоставлено хранилище.")

        res = self._scrapper(url=self.url, depth=depth, filtered=filtered)

        db = self._database()
        db.prepare_database()

        root_id = db.add("root", {"url": self.url})
        if root_id is None:
            fetched_id = db.fetch('root', ['id'], {"url": self.url})
            if fetched_id:
                root_id = fetched_id[0][0]
            else:
                logger.error(f"Ошибка добавления/чтения {self.url}")
                sys.exit(-1)

        try:
            for data in res.parse():
                data["root_id"] = root_id
                db.add("page", data)

                if self.display_info:
                    print(f'{data["url"]}: "{data["title"]}"')
                max_memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
                print(f'Memory usage: {max_memory_used} Mb\n')
        except KeyboardInterrupt:
            print("\nСбор данных прерван пользователем.")

    def get(self, limit: int = 50) -> None:
        """
        Отображает в терминале дынные из хранилища.
        :param limit: количество отображаемых данных.
        """
        if self._database is None:
            raise RepositoryNotPresented("Не предоставлено хранилище.")

        db = self._database()
        db.prepare_database()

        fetched_id = db.fetch('root', ['id'], {"url": self.url})
        if fetched_id:
            root_id = fetched_id[0][0]
        else:
            logger.error(f"Не найдено {self.url}")
            sys.exit(-1)

        result = db.fetch('page', ['url', 'title'], filters={"root_id": root_id}, limit=limit)
        for res in result:
            print(f'{res[0]}: "{res[1]}"')

    def set_scrapper(self, scrapper: Type[AbstractScrapper]):
        """ Устанавливает скраппер. """
        self._scrapper = scrapper

    def set_database(self, database: Type[AbstractRepository]):
        """ Устанавливает хранилище. """
        self._database = database


def main() -> None:
    """
    На основании переданных аргументов командной строки,
    конфигурирует Spyder под требуемую задачу и запускает на выполнение.
    """
    cli_params = get_args()
    if cli_params:
        spyder = Spider(url=cli_params["url"])

        if cli_params["method"] == "load":
            if cli_params["depth"] > 2:
                logger.info("Глубина обхода не может быть больше 2.")
                cli_params["depth"] = 2
            spyder.set_scrapper(Scrapper)
            spyder.set_database(PostgreSQL)
            spyder.display_info = cli_params["display_info"]
            spyder.load(depth=cli_params["depth"], filtered=cli_params["filtered"])
        else:
            spyder.set_database(PostgreSQL)
            spyder.get(limit=cli_params["depth"])


if __name__ == '__main__':
    main()
