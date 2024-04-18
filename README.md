# Тестовое задание DNS

Задачей было создание API-сервиса для поиска кратчайшего пути между городами.

Использовались следующие библиотеки:
- _fastapi_ - для создания самого API
- _sqlalchemy_ - для работы с базой данных через ORM
- _asyncpg_ - асинхронный движок для работы с PostgreSQL
- _alembic_ - для управления миграциями базы данных
- _pytest_ - для написания автоматических тестов

## Схема базы данных

1) **Cities**
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный.
   - **name**: VARCHAR(255), UNIQUE.

2) **Routes**
   - **id**: INTEGER, PRIMARY KEY, автоинкрементный.
   - **from_city_id**: INTEGER, FOREIGN KEY, ссылается на `id` в таблице Cities.
   - **to_city_id**: INTEGER, FOREIGN KEY, ссылается на `id` в таблице Cities.
   - **distance**: INTEGER (расстояние между городами в выбранных единицах измерения).

Модели расположены в файле:  
[Модели](./api/src/models/fsp.py)

## Создание миграций

Миграции расположены в директории:  
[Миграции](./api/src/migrations/versions/)

**Процесс создания миграций**
1) Начальная миграция моделей была выполнена с использованием Alembic. Название миграции: _init_.
2) В ходе тестирования выяснилось, что имена в таблице **Cities** должны быть уникальными, была создана миграция _cities_name_unique_.
3) Добавление данных из файла `sample.txt` выполнено миграцией _add_initial_data_.

## Создание эндпоинтов

Файлы эндпоинтов расположены в директории:  
[Эндпоинты](./api/src/api/)

Полное описание и примеры использования можно найти в файле:  
[Описание использования](./api/README.md)

## Выбранный архитектурный подход для API

Слоистая архитектура

Директории и файлы:
- Один файл с моделями городов и маршрутов между ними:  
  [Модели](./api/src/models/)

- Один файл содержит два репозитория, CitiesRepository и RoutesRepository, определяющие методы для добавления новых данных в модели Cities и Routes:  
  [Репозиторий](./api/src/repositories/)

- Cхемы Pydantic:  
  [Схемы](./api/src/schemas/)

- Сервисы, где происходит бизнес-логика. Метод `shortest_path` в сервисе CitiesService использует алгоритм Дейкстры для поиска кратчайшего пути:  
  [Сервисы](./api/src/services/)

- Два файла Утилиты:
- 1) В файле `repository.py` описаны базовые репозитории.
- 2) В файле `unitofwork.py` описан класс для управления данными и транзакциями:  
  [Утилиты](./api/src/utils/)

## Запуск проекта

Требуется установленный docker и docker-compose.

**Создание файла с переменными окружения**

```cmd
cp .env.example .env
```

**Запуск Тестов**

Linux и MacOS

```
make test
```


Windows

```
docker-compose -f docker-compose.test.yml up --build --force-recreate
```


**Запуск Проекта**

Linux и MacOS

```
make dev
```


Windows

```
docker-compose -f docker-compose.dev.yml up --build --force-recreate
```

# Задание 2

Задача заключалась в написании **SQL** запроса, который будет вычислять разницу в расстояниях между ближайшими по алфавиту целевыми городами для прямых маршрутов из города `city`.

```sql
WITH SortedRoutes AS (
    SELECT
        r.distance,
        c.name as destination_city,
        ROW_NUMBER() OVER (ORDER BY c.name) as rank
    FROM
        routes r
        JOIN cities c ON r.to_city_id = c.id
        JOIN cities from_city ON r.from_city_id = from_city.id
    WHERE
        from_city.name = :city
)
SELECT
    ABS(first.distance - second.distance) as distance_difference
FROM
    SortedRoutes first
    JOIN SortedRoutes second ON first.rank = second.rank - 1
WHERE
    first.rank = 1;
```

Не забудьте заменить `:city` в SQL запросе на название города, для которого будут проводиться вычисления.