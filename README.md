# Telegram Polls & Social Experiments

MVP-платформа для создания и прохождения опросов через Telegram-бота.

## Стек
- Backend: FastAPI + SQLAlchemy + PostgreSQL + Redis
- Bot: aiogram 3.x
- Infra: Docker Compose

## Быстрый старт
```bash
docker compose up --build
```

Сервисы:
- API: http://localhost:8000/docs
- Bot: запускается отдельным контейнером
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Переменные окружения
Скопируйте `.env.example` в `.env` и заполните значения.

## Что реализовано
- Регистрация пользователей через API
- CRUD для опросов (создание, просмотр, список пользователя, удаление)
- Добавление вопросов в опрос и получение списка вопросов
- Сохранение ответов (с защитой от повторных ответов на уровне вопроса)
- Базовая аналитика по опросу
- A/B-эксперимент (распределение по вариантам)
- Telegram-бот: `/start`, `/create_poll`, `/my_polls`, `/take_poll`, `/results`
