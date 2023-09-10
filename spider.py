"""
spider.py load http://www.vesti.ru/ --depth 2
>> ok, execution time: 10s, peak memory usage: 100 Mb
spider.py get http://www.vesti.ru/ -n 2
>> http://www.vesti.ru/news/: "Вести.Ru: новости, видео и фото дня"
>> http://www.vestifinance.ru/: "Вести Экономика: Главные события российской и мировой экономики, деловые новости,
фондовый рынок"

"""
import sys
from typing import Type

from utilites import resource_monitor, get_args
from scrapper import BaseScrapper, Scrapper
from database import AbstractRepository, PostgreSQL
from exceptions import ScrapperNotPresented, RepositoryNotPresented
from logger_config import logger


url = "https://ria.ru"
# url = "http://www.vesti.ru"
# url = "http://tass.ru/ural"
# url = "https://lenta.ru"


class Spyder:
    def __init__(self, url: str):
        self.url = url
        self._scrapper: Type[BaseScrapper] | None = None
        self._database: Type[AbstractRepository] | None = None

    @resource_monitor
    def load(self, depth: int = 0, filtered: bool = True):
        if self._scrapper is None:
            raise ScrapperNotPresented
        if self._database is None:
            raise RepositoryNotPresented

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

        for data in res.parse():
            data["root_id"] = root_id
            db.add("page", data)

    def get(self, limit: int = 50):
        if self._database is None:
            raise RepositoryNotPresented

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

    def set_scrapper(self, scrapper: Type[BaseScrapper]):
        self._scrapper = scrapper

    def set_database(self, database: Type[AbstractRepository]):
        self._database = database


def main():
    cli_params = get_args()
    spyder = Spyder(url=cli_params["url"])

    if cli_params["method"] == "load":
        if cli_params["depth"] > 2:
            logger.info("Глубина обхода не может быть больше 2.")
            cli_params["depth"] = 2
        spyder.set_scrapper(Scrapper)
        spyder.set_database(PostgreSQL)
        spyder.load(depth=cli_params["depth"], filtered=True)
    else:
        spyder.set_database(PostgreSQL)
        spyder.get(limit=cli_params["depth"])


if __name__ == '__main__':
    main()
