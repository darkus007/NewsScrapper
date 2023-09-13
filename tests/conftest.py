import pytest


@pytest.fixture
def test_html():
    with open('tests/index.html', 'r') as file:
        return file.read()
