# YaMDb API

REST API сервис публикации отзывов на произведения.

Проект реализуется как монолитное Django-приложение с использованием Django REST Framework.

## 📌 Текущий статус

Реализована базовая система пользователей и аутентификации:

* регистрация пользователей
* подтверждение регистрации по email
* получение JWT-токена
* авторизация через JWT
* управление пользователями
* кастомная модель пользователя
* базовая настройка прав доступа и пагинации

Доменная логика отзывов находится в разработке.

## 🚀 Реализованная функциональность

### 🔐 Аутентификация и регистрация

* Регистрация:
  `POST /api/v1/auth/signup/`
* Отправка кода подтверждения на email
* Получение JWT-токена:
  `POST /api/v1/auth/token/`
* Аутентификация по JWT
* Подключён Simple JWT
* Доступ к защищённым ресурсам — только для аутентифицированных пользователей

### 👤 Пользователи

* Кастомная модель `User`

  * расширена полями:

    * `bio`
    * `role`
* Добавлена в Django Admin
* Реализованы эндпоинты ресурса `users`
* Созданы `APIView`, `ViewSet` и сериализаторы
* Реализован кастомный permission:

  * `CustomIsAdminUser`

### ⚙️ Настройки проекта

* Подключена JWT-аутентификация
* Настроена `PageNumberPagination`
* Настроены права доступа
* Настроен email backend:

  * отправка в консоль
  * отправка в файл

## 🛠 Технологический стек

* Python 3.14
* Django
* Django REST Framework
* Simple JWT
* uv
* ruff

## 📂 Структура проекта

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
├── api/
├── reviews/
├── users/
└── yamdb/
```

## ⚙️ Конфигурация

Проект использует `.env` для хранения переменных окружения.
Пример переменных доступен в `.env.example`.

## 🚀 Установка и запуск

### Через uv (рекомендуется)

```bash
git clone https://github.com/whymello/yamdb_api.git
cd yamdb_api
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

### Через pip

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

Текущая версия: **0.2.0**

> 0.2.0 — реализована система пользователей и JWT-аутентификация.

Проект развивается инкрементально.
