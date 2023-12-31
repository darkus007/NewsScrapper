# News scrapper 

![Project language][badge_language]
![Docker][badge_docker]

Сервис, который обходит произвольный сайт с глубиной до 2 и сохраняет `html`, `url` и `title` страницы в хранилище.

### Архитектурные решения. 
При построении сервиса применены принципы проектирования SOLID и паттерны ООП. \
Глобально сервис состоит из трёх частей. 
1. Пакет `scrapper` содержит логику сбора данных. При этом получение HTML страницы выделено в отдельный класс, который в качестве аргумента передаётся в основной класс при его инициализации. 
2. Пакет `database` предоставляет интерфейс для работы с системой хранения данных (AbstractRepository). 
3. Модуль `spider.py` содержит класс `Spider`  который реализует логику бизнес задачи, для чего в качестве инструментов использует описанные выше пакеты `scrapper` и `database`. 

### Детали реализации.
Пакет `scrapper` содержит:
* `AbstractScrapper` - абстрактный класс скраппера для обеспечения инверсии зависимостей. 
* `BaseScrapper` - дочерний класс от `AbstractScrapper`, реализует логику сбора данных. В качестве аргумента принимает класс для получения HTML страниц из интернета. Данные отдаёт генератор по одной странице по мере их получения, что позволяет сильно экономить потребление памяти.   
* `AbstractHtmlSupplier` - абстрактный класс для получения HTML страниц, обеспечивает инверсию зависимостей. 
* `RequestsHtmlSupplier` - реализует логику получения HTML страницы с использованием библиотеки requests. С целью избежать блокировок, данный класс содержит небольшие задержки между запросами (которые можно установить в константах модуля), более задержек нет и скорость работы в рамках пакета scrapper ограничена только счетными операциями (быстродействием процессора). 

Архитектурные решения позволяют написать другой поставщик HTML страниц (с учётом имеющейся на предприятии инфраструктуры), 
например более быстрый с использованием пула подключений с разными адресами и без применения задержек. 
И заменить существующий `RequestsHtmlSupplier` без изменения остального кода сервиса, тем самым увеличить скорость работы всего приложения. 

Пакет `database` содержит:
* `AbstractRepository` абстрактный класс для работы с системой хранения данных, обеспечивает инверсию зависимостей. 
* `PostgreSQL` реализация системы хранения данных на PostgreSQL. 

Архитектурное решение позволяет легко менять базу данных не переписывая код сервиса, 
а только добавляя реализации системы хранения в других БД. 

Модуль `spider.py` содержит:
* Класс `Spider`, который на основании принятых параметров реализует логику сбора данных и сохранения в хранилище, вывод данных из хранилища.  
Содержит методы, которые задают классы `AbstractScrapper` и `AbstractRepository`, что позволяет динамически настраивать поведение класса в ходе выполнения программы под конкретную задачу. 
* Функция `main`, которая на основе переданных пользователем аргументов создаёт, настраивает и запускает на выполнение экземпляр класса `Spider`. 

### CLI (command line interface):
* По URL сайта и глубине обхода загружаются данные.
* По URL сайта из хранилища можно получить `n` прогруженных страниц (`url` и `title`).

Пример:
```bash
$ spider.py load http://www.vesti.ru --depth 1 -f -s
$ ok, execution time: 100s, peak memory usage: 25 Mb
```
где: \
`--depth 1` - глубина обхода страниц (0 - только главная страница, 1 - главная страница и все ссылки с нее, ...); \
`-f` - фильтровать по доменному имени сайта, необязательный параметр (в примере `vesti`); \
`-s` - динамически отображает собранные данные, необязательный параметр.

```bash
$ spider.py get http://www.vesti.ru -n 10
$ http://www.vesti.ru/news/: "Вести.Ru: новости, видео и фото дня"
$ http://www.vestifinance.ru/: "Вести Экономика: Главные события российской и мировой экономики, деловые новости, фондовый рынок"
```
где `-n` - количество выводимой информации (в примере 10 записей).

### Установка и запуск
Получаем приложение из репозитория
```bash
$ git clone https://github.com/darkus007/NewsScrapper.git
```
Далее с использованием Makefile
```bash
$ make build
$ make start
$ make shell
$ spider.py load http://www.vesti.ru --depth 0 -f -s
>> http://www.vesti.ru/: "Вести.Ru: новости, видео и фото дня"
>> ok, execution time: 0s, peak memory usage: 3 Mb
$ spider.py get http://www.vesti.ru -n 10
>> http://www.vesti.ru/: "Вести.Ru: новости, видео и фото дня"
```
Без использования Makefile

```bash
$ docker-compose up -d --build
$ docker-compose run --rm app sh
$ spider.py load http://www.vesti.ru --depth 0 -f -s
>> http://www.vesti.ru/: "Вести.Ru: новости, видео и фото дня"
>> ok, execution time: 0s, peak memory usage: 3 Mb
$ spider.py get http://www.vesti.ru -n 10
>> http://www.vesti.ru/: "Вести.Ru: новости, видео и фото дня"
```

Запуск тестов
```bash
$ make test
$ docker-compose run --rm app python -m pytest -v
```

Очистка системы
```bash
$ make clean
$ docker-compose down -v
```