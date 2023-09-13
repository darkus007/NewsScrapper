import pytest

from scrapper.scrapper import BaseScrapper, HtmlSupplierNotPresented
from scrapper.html_suppliers import AbstractHtmlSupplier


class TestHtmlSupplier(AbstractHtmlSupplier):
    def get(self, url: str, params=None) -> str:
        with open('tests/index.html') as file:
            return file.read()


class TestBaseScrapper:

    @pytest.mark.parametrize(
        "url, expected",
        [
            ("http://some.ru", "some"),
            ("http://some.ru/", "some"),
            ("https://some.ru/", "some"),
            ("http://www.some.com/", "some"),
            ("https://www.some.com/", "some"),
        ]
    )
    def test_get_root_from_domain_name(self, url, expected):
        result = BaseScrapper("http://some.ru").get_root_from_domain_name(url)
        assert result == expected

    def test_get_links_from_page_and_get_prepared_links_with__filtered_is_true(self, test_html):
        bs = BaseScrapper("http://test.ru", filtered=True)
        result = bs._get_links_from_page(test_html)
        assert result == {'http://test.ru', 'http://test.ru/sport/'}

    def test_get_links_from_page_and_get_prepared_links__filtered_is_false(self, test_html):
        bs = BaseScrapper("http://test.ru", filtered=False)
        result = bs._get_links_from_page(test_html)
        assert result == {'http://yandex.ru', 'http://test.ru/sport/', 'http://test.ru'}

    def test_parse(self):
        expected = {'title': 'Test title main page',
                    'url': 'http://test.ru',
                    'html': '<!DOCTYPE html>\n<html lang="en">\n'
                            '<head>\n    '
                                '<meta charset="UTF-8">\n    '
                                '<title>Test title main page</title>\n'
                            '</head>\n'
                            '<body>\n    '
                                '<a href="http://test.ru"></a>\n    '
                                '<a href="http://yandex.ru"></a>\n    '
                                '<a href="/sport/"></a>\n    '
                                '<a href="http://test.ru"></a>\n'
                            '</body>\n'
                    '</html>'}
        bs = BaseScrapper("http://test.ru")
        bs.html_supplier = TestHtmlSupplier()
        res = bs.parse().__next__()
        assert res == expected

    def test_parse_html_supplier_not_present(self):
        with pytest.raises(HtmlSupplierNotPresented):
            bs = BaseScrapper("http://test.ru")
            bs.parse().__next__()
