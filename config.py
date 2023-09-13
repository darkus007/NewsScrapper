"""
Загружает настройки для проекта.

Использован пакет dotenv:
    pip install python-dotenv
"""

from os import getenv

from dotenv import load_dotenv


load_dotenv()

DB_NAME = getenv('POSTGRES_DB')
DB_USER = getenv('POSTGRES_USER')
DB_PASS = getenv('POSTGRES_PASSWORD')
DB_HOST = getenv('POSTGRES_HOST')
DB_PORT = getenv('POSTGRES_PORT')

TEST_DB_NAME = getenv('TEST_POSTGRES_DB')
TEST_DB_USER = getenv('TEST_POSTGRES_USER')
TEST_DB_PASS = getenv('TEST_POSTGRES_PASSWORD')
TEST_DB_HOST = getenv('TEST_POSTGRES_HOST')
TEST_DB_PORT = getenv('TEST_POSTGRES_PORT')
