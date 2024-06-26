# FSP Service API Documentation

## Описание

FSP Service — это FastAPI приложение, которое помогает пользователю находить кратчайшее расстояние между городами. Этот сервис предоставляет API для управления городами и маршрутами, а также для поиска кратчайшего пути между ними.

## API Endpoints

### Города

- **GET /cities**
  - Описание: Получение списка всех городов.
  - Ответ: Возвращает массив городов с их ID и названиями.
  
- **POST /cities**
  - Описание: Добавление нового города в список.
  - Тело запроса: `{ "name": "Название города" }`
  - Ответ: Возвращает ID добавленного города.
  - Ошибки: Возвращает ошибку, если название города не предоставлено.

### Маршруты

- **GET /road**
  - Описание: Получение списка всех маршрутов.
  - Ответ: Возвращает массив маршрутов с ID начального и конечного города, а также дистанцией между ними.

- **POST /road**
  - Описание: Добавление нового маршрута.
  - Тело запроса: `{ "from_city_id": ID города отправления, "to_city_id": ID города назначения, "distance": расстояние }`
  - Ответ: Возвращает ID созданного маршрута.
  - Ошибки: Возвращает ошибку, если одно из полей не предоставлено.

### Поиск кратчайшего пути

- **GET /cities/{city}/findShortestPath**
  - Описание: Поиск кратчайшего пути между двумя городами.
  - Параметры: `city` (ID или название города отправления), `to` (ID или название города назначения).
  - Ответ: Возвращает информацию о пути, включая общую дистанцию и целевой город.

## Модели данных

### CitiesSchema
- `id`: ID города (integer)
- `name`: Название города (string)

### RoutesSchema
- `id`: ID маршрута (integer)
- `from_city_id`: ID города отправления (integer)
- `to_city_id`: ID города назначения (integer)
- `distance`: Расстояние между городами (integer)

## Валидация и ошибки

- **HTTPValidationError**: Возвращается, когда входные данные не соответствуют ожидаемым форматам.
  - `detail`: Подробное описание ошибок валидации.
  - `loc`: Местоположение ошибки в запросе.
  - `msg`: Сообщение об ошибке.
  - `type`: Тип ошибки.

## Примеры использования

### Получение списка всех городов

Запрос:
```
GET /cities
```

Ответ:
```json
[
  {"id": 1, "name": "Москва"},
  {"id": 2, "name": "Санкт-Петербург"}
]
```

### Добавление нового города
Запрос:
```
POST /cities
Content-Type: application/json

{
  "name": "Новосибирск"
}
```

```json
{
  "id": 3
}
```
