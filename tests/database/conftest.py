import psycopg2
import pytest

from config import TEST_DB_USER, TEST_DB_PASS, TEST_DB_NAME, TEST_DB_PORT, TEST_DB_HOST

DATABASE_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

test_connection = psycopg2.connect(DATABASE_URL)


@pytest.fixture(scope="package")
def connection_for_test():
    return test_connection


@pytest.fixture(scope="package", autouse=True)
def create_db():

    cursor = test_connection.cursor()
    with open('database/createdb.sql', 'r') as file:
        sql = file.read()
    cursor.execute(sql)
    test_connection.commit()

    yield

    with test_connection.cursor() as cursor:
        cursor.execute("DROP TABLE page;")
        test_connection.commit()
    with test_connection.cursor() as cursor:
        cursor.execute("DROP TABLE root;")
        test_connection.commit()
