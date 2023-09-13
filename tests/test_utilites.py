"""
Тестируем модуль utilites.py

Перехватываем вывод в консоль:
https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html
"""

from utilites import resource_monitor


def test_resource_monitor(capsys):
    @resource_monitor
    def some_func():
        pass

    some_func()

    captured = capsys.readouterr()
    assert 'ok, execution time:   0s, peak memory usage:   0 Mb\n' == captured.out
