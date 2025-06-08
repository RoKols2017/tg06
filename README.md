# Finance Bot 🤖

A fully‑asynchronous **Telegram wallet bot** that fetches official Central Bank of Russia (CBR) exchange rates and logs personal expenses using **aiogram 3**, **aiohttp** and **async SQLAlchemy**.

---

## ✨ Features

| Area | Description |
|------|-------------|
| **Exchange rates** | Live USD / EUR → RUB via <https://www.cbr-xml-daily.ru/> (no API key required) |
| **Expense tracking** | Two‑step FSM wizard (`category → amount`) writes records per user |
| **Persistence** | Async SQLAlchemy 2 with SQLite by default; switch to PostgreSQL via `DATABASE_URL` |
| **Config** | Secrets loaded from `.env` with `pydantic‑settings`; nothing hard‑coded |
| **Stack** | 100 % asyncio: `aiogram 3.20`, `aiohttp 3`, `SQLAlchemy 2`, `pydantic v2` |
| **Container‑ready** | `Dockerfile` + `docker‑compose.yml` provided |
| **Tests** | `pytest` with aiogram‑pytest‑plugin, 100 % async |

---

## 🗂️ Project Layout

```
finance-bot/
├─ app/                    # main package
│  ├─ main.py              # entry‑point
│  ├─ config.py            # settings via .env
│  ├─ handlers/            # routers: common, auth, rates, finance
│  ├─ db/                  # models.py, session.py
│  ├─ utils/               # exchange.py (CBR client)
│  └─ keyboards/           # reply / inline menus
├─ .env.example            # sample secrets
├─ pyproject.toml
└─ README.md               # you're here
```

---

## 🚀 Quick Start

```bash
# clone & enter
git clone https://github.com/your‑nick/finance-bot.git
cd finance-bot

# Python 3.12+ virtualenv
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# configure secrets
cp .env.example .env
nano .env           # add BOT_TOKEN, DATABASE_URL if needed

# run
python -m app.main
```

### With Docker

```bash
docker compose up --build
```

---

## 🔧 Environment Variables

| Variable | Required | Example | Note |
|----------|----------|---------|------|
| `BOT_TOKEN` | ✅ | `123456:ABC...` | Token from BotFather |
| `DATABASE_URL` | ⬜ | `sqlite+aiosqlite:///./finance.db` | Defaults to SQLite |
| `LOG_LEVEL` | ⬜ | `INFO` | Root logging level |

---

## 📝 Bot Commands

| Command / Button | Action |
|------------------|--------|
| `/start`, **Main menu** | Show help and buttons |
| **💳 Register** | Create account in DB |
| **�� Rates** | Show USD / EUR to RUB |
| **📊 Expenses** | FSM: *category → amount* |
| `/summary`* | *(planned)* monthly totals |

---

## 🛠️ Tech Stack

* Python 3.12+
* **aiogram 3.20.0post0**
* **aiohttp 3.9+**
* **SQLAlchemy 2.0 async**
* **pydantic 2.11**, **pydantic‑settings 2.9**
* SQLite / PostgreSQL
* Docker / docker‑compose
* pytest, ruff, mypy

---

## 🛤 Roadmap

- [ ] Inline editing / deleting expenses  
- [ ] Monthly summary report `/summary`  
- [ ] Matplotlib charts  
- [ ] Redis storage for FSM  
- [ ] Deploy to Fly.io template  

---

## 🤝 Contributing

1. Fork repo and create feature branch:  
   `git checkout -b feat/amazing‑feature`
2. Commit your changes with conventional commits.
3. Run `ruff check .`, `mypy .`, `pytest`.
4. Open a Pull Request.

---

## 📄 License

MIT © 2025 RoKols.  
See `LICENSE` for details.

---

## 🗄️ Создание таблиц БД

Перед первым запуском бота необходимо создать все таблицы в базе данных. Для этого выполните:

```bash
python -m app.create_tables
```

- Скрипт создаст все необходимые таблицы согласно ORM-моделям в `app/db/models.py`.
- Используется асинхронный движок SQLAlchemy (см. настройки в `.env` или по умолчанию SQLite).

---

## 🚦 Правильный запуск проекта

Для запуска бота используйте команду:

```bash
python -m app.main
```

- Убедитесь, что все зависимости установлены (`pip install -r requirements.txt`).
- Проверьте, что переменные окружения заданы в `.env` (см. раздел выше).
- Для работы с GigaChat и курсами валют необходимы соответствующие API-ключи.

---

## 🌐 Подключение внешних API

Бот использует несколько внешних API для своей работы:

### 1. GigaChat (генерация советов)
- Для интеграции с GigaChat необходим токен (`GIGACHAT_TOKEN`).
- Получить токен можно на https://developers.sber.ru/gigachat/.
- Переменные окружения:
  - `GIGACHAT_TOKEN` — токен доступа (обязателен для генерации советов через GigaChat).
  - `VERIFY_SSL_CERTS` — проверять SSL-сертификаты (по умолчанию True).
- Если токен не указан, советы будут выдаваться из локального списка.

### 2. ExchangeRate API (курсы валют)
- Для получения курсов USD/EUR к рублю используется ExchangeRate API.
- Получить ключ: https://www.exchangerate-api.com/
- Переменная окружения:
  - `EXCHANGE_API_KEY` — API-ключ для доступа к ExchangeRate API (обязателен).

---

## 🏗️ Подробная структура проекта

```
app/
├── __init__.py           # Описание пакета приложения
├── main.py               # Точка входа, запуск aiogram-бота
├── config.py             # Конфигурация и загрузка переменных окружения
├── create_tables.py      # Скрипт для создания всех таблиц БД
│
├── db/                   # Работа с базой данных
│   ├── __init__.py
│   ├── models.py         # ORM-модели (User, Category)
│   └── session.py        # Асинхронный engine и sessionmaker
│
├── handlers/             # Обработчики команд и сообщений
│   ├── __init__.py
│   ├── auth.py           # Регистрация пользователей
│   ├── common.py         # Старт, помощь, советы
│   ├── finance.py        # Учёт расходов (FSM)
│   └── rates.py          # Курс валют
│
├── keyboards/            # Клавиатуры Telegram-бота
│   ├── __init__.py
│   └── main.py           # Главное меню
│
├── utils/                # Утилиты и вспомогательные функции
│   ├── __init__.py
│   ├── exchange.py       # Работа с ExchangeRate API
│   ├── gigachat.py       # Интеграция с GigaChat
│   └── messages.py       # Текстовые сообщения и советы
```

- **app/main.py** — запуск бота, настройка логирования, регистрация роутеров.
- **app/config.py** — загрузка и валидация переменных окружения через pydantic-settings.
- **app/create_tables.py** — отдельный скрипт для создания таблиц БД (используйте перед первым запуском).
- **app/db/** — все, что связано с моделями и сессиями БД.
- **app/handlers/** — обработчики команд, разбитые по смыслу.
- **app/keyboards/** — генерация клавиатур для Telegram.
- **app/utils/** — интеграция с внешними API, текстовые сообщения, советы.
