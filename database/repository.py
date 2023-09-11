from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def __init__(self, *args):
        ...

    @abstractmethod
    def add(self, table_name: str, data: dict) -> int | None:
        ...

    @abstractmethod
    def fetch(self,
              table: str,
              columns: list[str],
              filters: dict | None = None,
              limit: int = 50,
              offset: int = 0
              ) -> list[tuple | None]:
        ...

    @abstractmethod
    def prepare_database(self) -> None:
        ...
