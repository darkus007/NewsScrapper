"""
spider.py load http://www.vesti.ru/ --depth 2
>> ok, execution time: 10s, peak memory usage: 100 Mb
spider.py get http://www.vesti.ru/ -n 2
>> http://www.vesti.ru/news/: "Вести.Ru: новости, видео и фото дня"
>> http://www.vestifinance.ru/: "Вести Экономика: Главные события российской и мировой экономики, деловые новости,  фондовый рынок"

"""
import gc
import tracemalloc
from time import time

from scrapper.scrapper import Scrapper


url = "https://ria.ru"
# url = "http://www.vesti.ru"
# url = "http://tass.ru/ural"
# url = "https://lenta.ru"


# starting the monitoring
tracemalloc.start()
start_time = time()

res = Scrapper(url=url, depth=1, filtered=True)
print(f"{res.root_base_url=}")

print("\nResult:")
for data in res.parse():
    print(data["title"])
    print(data["url"])
    print(f"Memory: {tracemalloc.get_traced_memory()[1] / 1024 // 1024} Mb\n")
    gc.collect()


# displaying the memory
time_spend = time() - start_time
max_memory_used = tracemalloc.get_traced_memory()[1] / 1024 / 1024
print(f"Memory: {max_memory_used} Mb")
print(f"Time spend: {time_spend} second")
print('ok, execution time: {0:.0n}s, peak memory usage: {1:.0n} Mb'.format(time_spend, max_memory_used))
print('ok, execution time: {0:3.0n}s, peak memory usage: {1:3.0n} Mb'.format(time_spend, max_memory_used))

# stopping the library
tracemalloc.stop()
