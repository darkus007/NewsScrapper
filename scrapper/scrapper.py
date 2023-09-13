import re
from collections import deque
from collections.abc import Generator
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from .html_suppliers import AbstractHtmlSupplier, RequestsHtmlSupplier


class HtmlSupplierNotPresented(Exception):
    pass


class AbstractScrapper(ABC):
    @abstractmethod
    def __init__(self, url: str, depth: int, filtered: bool):
        ...

    @abstractmethod
    def parse(self):
        ...


class BaseScrapper(AbstractScrapper):

    html_supplier: AbstractHtmlSupplier = None

    def __init__(self, url: str, depth: int = 0, filtered: bool = True):
        self.root_url = url
        self.depth = depth + 1
        self.root_base_url = self.get_root_from_domain_name(self.root_url) if filtered else None
        self.parsed_links = set()
        self.prepared_links = deque()

    @staticmethod
    def get_root_from_domain_name(base_url: str) -> str:
        return re.findall(r"http[s]{0,1}://[w]{0,3}[.]*(\w+)[.]", base_url)[0]

    def parse(self) -> Generator[dict]:
        """
        Запускает процесс сбора информации.
        Результат отдает по одной странице.

        :return: dict("title": str, "url": str, "html": str)
        """
        if self.html_supplier is None:
            raise HtmlSupplierNotPresented("Не предоставлен html supplier.")

        self.prepared_links.append(self.root_url)

        while self.depth > 0:
            self.depth -= 1

            for _ in self.prepared_links.copy():
                result = {}
                url = self.prepared_links.popleft()
                if html := self.html_supplier.get(url):
                    self.parsed_links.add(url)
                    soup = BeautifulSoup(html, 'lxml')
                    title = soup.find("title")
                    if title:
                        result["title"] = title.text
                        result["url"] = url
                        result["html"] = html
                        if self.depth:
                            links = self._get_links_from_page(html)
                            self.prepared_links.extend(links)
                        yield result

    def _get_links_from_page(self, html: str) -> set[str]:
        """
        Собирает ссылки со страницы.

        :param html: страница web-сайта в формате html.
        :return: Коллекция url-адресов.
        """
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all("a", href=True)
        return self._get_prepared_links([link["href"] for link in links])

    def _get_prepared_links(self, links: list[str]):
        """
        Проходит по всем собранным со страницы ссылкам
        и подготавливает их для парсинга:
        - добавляет корневой URL, если ссылка содержит только URI;
        - исключает уже обработанные, ссылки;
        - фильтрует по домену, если filtered = True.

        :param links: все собранные со страницы ссылки.
        :return: Подготовленные к парсингу url ссылки.
        """
        prepared_links = set()
        for link in links:

            if "http" not in link:
                link = self.root_url + link

            if link in self.parsed_links:
                continue

            if self.root_base_url is not None:
                if self.root_base_url in link:
                    prepared_links.add(link)
                    continue
            else:
                prepared_links.add(link)

        return prepared_links


class Scrapper(BaseScrapper):
    html_supplier: AbstractHtmlSupplier = RequestsHtmlSupplier()
