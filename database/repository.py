from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, *args):
        ...

    @abstractmethod
    def add(self, table_name: str, data: dict) -> int | None:
        """
        Добавляет запись в базу данных.

        :param table_name: Название таблицы.
        :param data: Словарь для записи,
                    где ключ - поле таблицы,
                    а значение - данные для записи.
        :return: id добавленной записи.
        """
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def prepare_database(self) -> None:
        """
        Создает базу данных и таблицы в ней,
        если база и таблицы уже существуют,
        то ничего не делает.
        """
        ...
