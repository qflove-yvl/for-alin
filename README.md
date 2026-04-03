# Telegram Polls & Social Experiments

MVP-платформа для создания и прохождения опросов через Telegram-бота.

## Стек
- Backend: FastAPI + SQLAlchemy + PostgreSQL + Redis
- Bot: aiogram 3.x
- Infra: Docker Compose

## Куда вставлять токен Telegram-бота
**Токен нужно указать в файле `.env` в корне проекта.**

1. Скопируйте шаблон:
   ```bash
   cp .env.example .env
   ```
2. Откройте `.env` и заполните строку:
   ```env
   BOT_TOKEN=1234567890:AA...your_real_token...
   ```

> ⚠️ Не отправляйте токен никому (в чат, в git, в скриншоты). Если токен уже где-то засветился — перевыпустите его через BotFather.

## Быстрый старт
1. Подготовьте `.env` (см. раздел выше).
2. Запустите сервисы:
   ```bash
   docker compose up --build
   ```
3. Проверьте API:
   - Swagger: http://localhost:8000/docs
   - Healthcheck: http://localhost:8000/health

## Сервисы в docker-compose
- `backend` — FastAPI API
- `bot` — Telegram бот
- `postgres` — основная БД
- `redis` — кэш/состояния


## Если в PowerShell ошибка "docker не распознан"
Это означает, что Docker Desktop не установлен или не добавлен в PATH.

### Вариант A (рекомендуется): установить Docker Desktop
1. Установите Docker Desktop для Windows.
2. Перезапустите PowerShell.
3. Проверьте командой:
   ```powershell
   docker --version
   docker compose version
   ```
4. Затем снова запустите:
   ```powershell
   docker compose up --build
   ```

### Вариант B: запустить без Docker (локально)
Нужны отдельно установленные PostgreSQL + Redis + Python 3.11.

Backend:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Bot (в новом окне PowerShell):
```powershell
cd bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

## Первый запуск в Telegram
1. Откройте вашего бота в Telegram.
2. Отправьте `/start`.
3. Дальше используйте команды:
   - `/create_poll`
   - `/my_polls`
   - `/take_poll`
   - `/results <poll_id>`

## Что реализовано
- Регистрация пользователей через API
- CRUD для опросов (создание, просмотр, список пользователя, удаление)
- Добавление вопросов в опрос и получение списка вопросов
- Сохранение ответов (с защитой от повторных ответов на уровне вопроса)
- Базовая аналитика по опросу
- A/B-эксперимент (распределение по вариантам)
- Telegram-бот: `/start`, `/create_poll`, `/my_polls`, `/take_poll`, `/results`
