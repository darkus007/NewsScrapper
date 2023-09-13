import pytest

from scrapper import AbstractScrapper
from spider import Spider, ScrapperNotPresented, RepositoryNotPresented


class TestSpider:
    @pytest.mark.parametrize(
        "url, expected",
        [
            ("http://some.ru", "http://some.ru/"),
            ("http://some.ru/", "http://some.ru/")
        ]
    )
    def test_add_slash_to_url(self, url: str, expected: str):
        spider = Spider(url)
        assert spider.url == expected

    def test_scrapper_not_presented_exception(self):
        spider = Spider("some")
        with pytest.raises(ScrapperNotPresented):
            spider.load()

    def test_repository_not_presented_exception_load(self):
        class FakeScrapper(AbstractScrapper):
            def __init__(self):
                pass

            def parse(self):
                pass

        spider = Spider("some")
        spider.set_scrapper(FakeScrapper)
        with pytest.raises(RepositoryNotPresented):
            spider.load()

    def test_repository_not_presented_exception_get(self):
        spider = Spider("some")
        with pytest.raises(RepositoryNotPresented):
            spider.get()
