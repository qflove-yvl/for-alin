# Telegram Polls & Social Experiments

MVP-платформа для создания и прохождения опросов через Telegram-бота.

## Стек
- Backend: FastAPI + SQLAlchemy + PostgreSQL + Redis
- Bot: aiogram 3.x
- Infra: Docker Compose

## Запуск одной командой (как ты и просил)
1. Установи Python 3.11+
2. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запусти всё одной командой:
   ```bash
   python app.py
   ```

Что делает `app.py`:
- создаёт `.env` из `.env.example`, если файла нет;
- запускает backend на `http://127.0.0.1:8000`;
- ждёт healthcheck;
- запускает Telegram-бота.
- автоматически ставит `API_BASE_URL=http://127.0.0.1:8000` для локального режима (чтобы не было `backend:8000` ошибок);
- в режиме `python app.py` по умолчанию использует локальную SQLite (`local.db`) — чтобы старт был без PostgreSQL;
- если нужен строго PostgreSQL, запусти: `APP_USE_POSTGRES=1 python app.py` (или через Docker Compose).

> Перед запуском обязательно пропиши реальный `BOT_TOKEN` в `.env`.

## Запуск в России (когда Telegram заблокирован)
Если `api.telegram.org:443` недоступен, используй прокси/VPN и передай его боту через `.env`.

### Вариант 1 (самый простой): системный VPN
1. Включи рабочий VPN на ПК (WARP, AmneziaWG, Outline и т.д.).
2. Запусти:
   ```bash
   python app.py
   ```

### Вариант 2: прокси только для бота
В `.env` укажи прокси:
```env
TELEGRAM_PROXY=http://127.0.0.1:8080
# или
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```

После изменения `.env` перезапусти:
```bash
python app.py
```

Проверка, что бот видит прокси:
- в логах должна исчезнуть ошибка `Cannot connect to host api.telegram.org:443`
- бот должен пройти `Start polling` без `Polling stopped`

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

## Очень простой запуск (рекомендуется)
### Windows (PowerShell)
```powershell
./scripts/dev-up.ps1 -BotToken "ВАШ_ТОКЕН"
```

### macOS/Linux
```bash
./scripts/dev-up.sh "ВАШ_ТОКЕН"
```

Скрипт сам:
- создаст `.env`, если его нет;
- подставит `BOT_TOKEN`;
- запустит `docker compose up -d --build`.

Остановить всё:
```powershell
./scripts/dev-down.ps1
```
или
```bash
make down
```

## Быстрый старт
1. Рекомендуется подготовить `.env` (см. раздел выше):
   ```bash
   cp .env.example .env
   ```
2. Запустите сервисы:
   ```bash
   docker compose up --build
   ```
   > Если `.env` отсутствует, compose возьмёт значения из `.env.example` автоматически.
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


## Если бот падает с `Cannot connect to host api.telegram.org:443`
Это сетевой доступ к Telegram API (не ошибка логики бота).

Проверьте:
1. Интернет на хосте и в Docker.
2. Корпоративный/домашний firewall или антивирус (может блокировать Docker).
3. VPN/прокси (в некоторых сетях без VPN Telegram недоступен).

Полезная диагностика:
```powershell
docker compose logs bot --tail=100
docker compose exec bot python -c "import socket; print(socket.gethostbyname('api.telegram.org'))"
```

В проекте добавлен автоповтор подключения: если сеть до Telegram временно недоступна,
бот теперь не завершается сразу, а пробует переподключиться каждые 5 секунд.


Если доступ к Telegram у провайдера блокируется, добавьте прокси в `.env`:
```env
TELEGRAM_PROXY=http://host.docker.internal:1080
```
(пример, подставьте ваш реальный HTTP/SOCKS5 proxy URL).

После изменения `.env` перезапустите:
```powershell
docker compose up -d --build bot
```

## Первый запуск в Telegram

После `/start` бот теперь сразу показывает список команд и кнопки меню.
1. Откройте вашего бота в Telegram.
2. Отправьте `/start`.
3. Дальше используйте команды:
   - `/help`
   - `/create_poll` (создаёт опрос и позволяет сразу добавить вопросы в чате)
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
