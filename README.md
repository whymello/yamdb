# YaMDb API

REST API сервис публикации отзывов на произведения.

Проект реализован как монолитное Django-приложение с использованием Django REST Framework.

## 📌 Статус проекта

✅ Основная функциональность полностью реализована  
✅ Проект готов к использованию и дальнейшему расширению  

## 🚀 Реализованная функциональность

### 🔐 Аутентификация и регистрация (Auth)

- Регистрация: `POST /api/v1/auth/signup/`
- Отправка кода подтверждения на email
- Получение JWT-токена: `POST /api/v1/auth/token/`
- Аутентификация по JWT
- Подключён Simple JWT
- Доступ к защищённым ресурсам — только для аутентифицированных пользователей

### 👤 Пользователи (Users)

- Кастомная модель `User` расширена полями `bio` и `role`

- Реализованы:

  - управление пользователями (`/api/v1/users/`)
  - получение и редактирование своего профиля (`/api/v1/users/me/`)

- Администратор может:

  - создавать пользователей
  - редактировать информацию пользователей
  - удалять пользователей

### 🎬 Категории (Categories)

- Эндпоинт: `/api/v1/categories/`
- Чтение — для всех  
- Создание / удаление — только для администратора  

### 🎭 Жанры (Genres)

- Эндпоинт: `/api/v1/genres/`
- Чтение — для всех  
- Создание / удаление — только для администратора  

### 🎬 Произведения (Titles)

- Эндпоинт: `/api/v1/titles/`

- Поддерживает:

  - просмотр
  - создание
  - редактирование
  - удаление

Рейтинг (`rating`) рассчитывается автоматически как **средняя оценка отзывов пользователей**.

### ✍️ Отзывы (Reviews)

- Эндпоинт: `/api/v1/titles/{title_id}/reviews/`

- Особенности:

  - один пользователь — один отзыв на произведение
  - оценка от 1 до 10

- Доступ:

  - чтение — для всех  
  - создание — для авторизованных  
  - изменение / удаление — автор, модератор или администратор  

### 💬 Комментарии (Comments)

- Эндпоинт: `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`

- Доступ:

  - чтение — для всех  
  - создание — для авторизованных  
  - изменение / удаление — автор, модератор или администратор  

## 📖 API документация

Автогенерируемая документация доступна после запуска проекта:

- Swagger UI: `/api/v1/swagger-ui/`
- ReDoc: `/api/v1/redoc/`
- OpenAPI схема: `/api/v1/schema/`

Документация реализована с помощью **drf-spectacular**.

## 📥 Импорт данных

В проекте реализована management-команда для импорта данных из CSV файлов.

Файлы должны находиться в директории `static/data/`.

Запуск команды:

```bash
uv run manage.py importcsv
```

или (с активированным окружением)

```bash
python manage.py importcsv
```

Импорт выполняется через ORM Django.

## ⚙️ Настройки проекта

- JWT-аутентификация
- PageNumberPagination
- кастомные permissions
- email backend:
  - консоль
  - файл

## 🛠 Технологический стек

- Python 3.14
- Django
- Django REST Framework
- Simple JWT
- drf-spectacular
- uv
- ruff

## 📂 Структура проекта

```bash
yamdb_api/
├── api/
├── reviews/
├── static/
├── users/
└── yamdb/
```

## ⚙️ Конфигурация

Проект использует `.env` для хранения переменных окружения.

Пример доступен в `.env.example`.

## 🚀 Установка и запуск

### Через uv (рекомендуется)

```bash
git clone https://github.com/whymello/yamdb_api.git
cd yamdb_api
uv sync
uv run manage.py migrate
uv run manage.py importcsv  # (опционально, для заполнения данными)
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
python manage.py importcsv  # (опционально, для заполнения данными)
python manage.py runserver
```

## 🔄 Версионирование

Текущая версия: **1.0.0**

```text
0.1.0 — инициализация проекта
0.2.0 — система пользователей и JWT-аутентификация
0.3.0 — ресурсы categories, genres, titles
0.4.0 — ресурсы reviews и comments
1.0.0 — завершённая версия API
```
