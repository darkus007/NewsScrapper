import psycopg2

from database.repository import AbstractRepository
from config import DB_USER, DB_PASS, DB_NAME, DB_PORT, DB_HOST

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

connection = psycopg2.connect(DATABASE_URL)


class PostgreSQL(AbstractRepository):
    def __init__(self, connect=connection):
        self.connect = connect

    def add(self, table: str, data: dict) -> int | None:
        """
        Добавляет запись в базу данных.

        :param table: Название таблицы.
        :param data: Словарь для записи,
                    где ключ - поле таблицы,
                    а значение - данные для записи.
        :return: int.
        """
        if len(data) > 1:
            html = psycopg2.Binary(bytes(data["html"], 'utf-8'))
            query = str(
                f"INSERT INTO {table} (root_id, title, url, html) "
                f"VALUES ({data['root_id']}, '{data['title']}', '{data['url']}', {html}) "
                f"ON CONFLICT (title, url) DO NOTHING "
                f"RETURNING id;"
            )
            query = query.replace('None', 'NULL')
        else:
            column = tuple(data.keys())[0]
            value = tuple(data.values())[0]
            query = str(
                f"INSERT INTO {table} ({column}) VALUES ('{value}') ON CONFLICT ({column}) DO NOTHING RETURNING id;"
            )
        cursor = self.connect.cursor()
        try:
            cursor.execute(query)
            self.connect.commit()
            new_id = cursor.fetchone()
            return new_id[0] if new_id else None
        except Exception as ex:
            print(f"Ошибка при записи в БД: {ex}")
            self.connect.rollback()
        finally:
            cursor.close()

    def fetch(self,
              table: str,
              columns: list[str],
              filters: dict | None = None,
              limit: int = 50,
              offset: int = 0
              ) -> list[tuple | None]:
        """
        Возвращает результаты из одной таблицы базы данных.

        :param table: Название таблицы.
        :param columns: Список с полями таблицы.
        :param filters: Словарь с фильтрами.
        :param limit: Количество записей.
        :param offset: Смещение от начала.
        :return: Список кортежей.
        """
        columns_joined = ", ".join(columns)
        with self.connect.cursor() as cursor:
            query = f"SELECT {columns_joined} FROM {table} "
            if filters:
                filter_pref = "WHERE"
                for key, value in filters.items():
                    filter_pref += " " + key + " = " + f"'{str(value)}'" + " "
                query += filter_pref
            last = f"ORDER BY id LIMIT {limit} OFFSET {offset}"
            query += last
            cursor.execute(query)
            return cursor.fetchall()

    def prepare_database(self) -> None:
        """
        Создает базу данных и таблицы в ней,
        если база и таблицы уже существуют,
        то ничего не делает.
        """
        with self.connect.cursor() as cursor:
            with open('database/createdb.sql', 'r') as file:
                sql = file.read()
            cursor.execute(sql)
            self.connect.commit()
