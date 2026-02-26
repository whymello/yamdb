# YaMDb API

Django-проект для разработки REST API сервиса публикации отзывов на произведения.

⚠️ Проект находится в начальной стадии разработки.
На данный момент создан только базовый Django-проект без реализованной бизнес-логики.

## 📌 Текущий статус

Инициализирован проект:

* создано виртуальное окружение через `uv`
* создан Django-проект
* базовая структура проекта без приложений

## 🛠 Технологический стек (на текущий момент)

* Python 3.14
* Django
* uv (dependency management)

## 📂 Структура проекта

Базовая структура Django:

```bash
yamdb_api/
├── manage.py
├── pyproject.toml
├── .python-version
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── uv.lock
└── yamdb/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## ⚙️ Конфигурация

Проект использует файл `.env` для хранения переменных окружения.
Пример доступен в `.env.example`.

## 🚀 Установка и запуск

### Рекомендуемый способ (через uv)

```bash
git clone https://github.com/whymello/yamdb_api.git
cd yamdb_api
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

### Альтернативный способ (через pip)

```bash
git clone https://github.com/whymello/yamdb_api.git
cd yamdb_api

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🔄 Версионирование

Текущая версия: **0.1.0**

Проект развивается инкрементально.
