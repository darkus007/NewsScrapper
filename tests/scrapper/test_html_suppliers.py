import requests

from scrapper.html_suppliers import RequestsHtmlSupplier


class MockResponse:
    status_code = 200

    # метод всегда возвращает определенный словарь для тестов
    @property
    def text(self):
        with open('tests/index.html') as file:
            return file.read()


class TestRequestsHtmlSupplier:
    def test_get(self, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests.Session, "get", mock_get)

        res = RequestsHtmlSupplier().get('http://test.ru')
        with open('tests/index.html') as file:
            assert res == file.read()
