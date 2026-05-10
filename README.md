# Flask Ads API

REST API для управления объявлениями на Flask + SQLAlchemy (SQLite).

## Структура проекта

```
flask_ads_project/
├── flask_ads/
│   ├── __init__.py       # Фабрика приложения (create_app)
│   ├── extensions.py     # Инициализация расширений (db)
│   ├── models.py         # Модель Advertisement
│   └── routes.py         # Маршруты /api/ads
├── app.py                # Точка входа
├── requirements.txt
├── .gitignore
└── README.md
```

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone <url>
cd flask_ads_project

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить приложение
python app.py
```

Сервер запустится на `http://127.0.0.1:5000`.  
База данных `ads.db` создаётся автоматически при первом запуске.

## Эндпоинты

| Метод  | URL              | Описание                    |
|--------|------------------|-----------------------------|
| POST   | /api/ads         | Создать объявление          |
| GET    | /api/ads         | Получить все объявления     |
| GET    | /api/ads/`<id>`  | Получить объявление по ID   |
| PUT    | /api/ads/`<id>`  | Обновить объявление         |
| DELETE | /api/ads/`<id>`  | Удалить объявление          |

## Примеры запросов

### Создать объявление

```bash
curl -X POST http://127.0.0.1:5000/api/ads \
  -H "Content-Type: application/json" \
  -d '{"title": "Продам велосипед", "description": "Горный, б/у", "owner": "Иван"}'
```

### Создать объявление без owner (подставится "anonymous")

```bash
curl -X POST http://127.0.0.1:5000/api/ads \
  -H "Content-Type: application/json" \
  -d '{"title": "Продам велосипед", "description": "Горный, б/у"}'
```

### Получить все объявления

```bash
curl http://127.0.0.1:5000/api/ads
```

### Получить по ID

```bash
curl http://127.0.0.1:5000/api/ads/1
```

### Обновить объявление

```bash
curl -X PUT http://127.0.0.1:5000/api/ads/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Продам велосипед (срочно)"}'
```

### Удалить объявление

```bash
curl -X DELETE http://127.0.0.1:5000/api/ads/1
```

Успешное удаление возвращает пустой ответ со статусом `204 No Content`.

## Модель данных

| Поле        | Тип      | Обязательное | Описание                              |
|-------------|----------|:------------:|---------------------------------------|
| id          | integer  | —            | Автоматически                         |
| title       | string   | ✓            | Заголовок объявления (макс. 200)      |
| description | text     | ✓            | Текст объявления                      |
| owner       | string   | —            | Владелец (по умолчанию `anonymous`)   |
| created_at  | datetime | —            | Время создания (UTC, ISO 8601)        |
