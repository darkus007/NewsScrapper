import tracemalloc
from sys import argv
from time import time
from typing import Callable
from functools import wraps

wellcome_cli_text = """
Проверьте параметры запуска. Доступны следующие варианты:
spider.py load https://ria.ru --depth 1 -s
spider.py get https://ria.ru -n 10
"""


def resource_monitor(func: Callable):
    """
    Отображает время работы функции и потребление памяти приложения.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time()

        res = func(*args, **kwargs)

        time_spend = time() - start_time
        max_memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
        print('ok, execution time: {0:3d}s, peak memory usage: {1:3d} Mb'
              .format(int(time_spend), int(max_memory_used))
              )

        tracemalloc.stop()

        return res

    return wrapper


def get_args() -> dict:
    """
    Парсит аргументы командной строки.
    :return: Словарь с параметрами.
    """
    args = argv[1:]
    if args[0] == "load" and args[2] == "--depth":
        return {"method": 'load', "url": args[1], "depth": int(args[3]),
                "display_info": True if '-s' in args else False}
    elif args[0] == "get" and args[2] == "-n":
        return {"method": 'get', "url": args[1], "depth": int(args[3])}
    else:
        print(wellcome_cli_text)
