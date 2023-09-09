import re
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from .mixins import RequestsMixin
from logger_config import logger


class BaseNewsScrapper(ABC):
    @abstractmethod
    def parse(self):
        ...


class Scrapper(BaseNewsScrapper, RequestsMixin):
    def __init__(self, url: str, depth: int = 0, filtered: bool = False):
        RequestsMixin.__init__(self)
        self.root_url = url
        self.depth = depth
        self.root_base_url = self.get_root_from_domain_name(self.root_url) if filtered else None
        self.parsed_links = set()
        self.result = []

    def parse(self):
        response = self.requests_get(self.root_url, timeout=1)
        if response and response.status_code == 200:
            self.parsed_links.add(self.root_url)
            soup = BeautifulSoup(response.text, 'lxml')
            self.result.append(
                {
                    "title": soup.find("title").text,
                    "url": response.url,
                    "html": response.text
                }
            )

            if self.depth:
                self.result = self._get_links_from_page(self.result)
            return self.result
        else:
            logger.error(f"Не удалось получить главную страницу: {self.root_url}")

    @staticmethod
    def get_root_from_domain_name(base_url: str) -> str:
        return re.findall(r"http[s]{0,1}://[w]{0,3}[.]*(\w+)[.]", base_url)[0]

    def _get_links_from_page(self, pages: list[dict]) -> list:
        self.depth -= 1
        output = []
        for page in pages:
            soup = BeautifulSoup(page["html"], 'lxml')

            links = soup.find_all("a", href=True)
            links = self._get_prepared_links([
                link["href"] for link in links
            ])

            for link in links:
                response = self.requests_get(link)
                self.parsed_links.add(link)
                if response and response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    title = soup.find("title")
                    if title:
                        output.append(
                            {
                                "title": title.text,
                                "url": response.url,
                                "html": response.text
                            }
                        )
        if self.depth:
            return pages + self._get_links_from_page(output)
        return output

    def _get_prepared_links(self, links: list[str]):
        """
        Проходит по всем собранным со странице ссылкам
        и подготавливает их для парсинга:
        - добавляет корневой URL, если ссылка содержит только URI;
        - исключает уже обработанные, ссылки;
        - фильтрует по домену, если filtered = True

        :param links: Все собранные со страницы ссылки.
        :return: Подготовленные к парсингу ссылки.
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
