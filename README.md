# 🗂️ Business CRM — CRM-система для малого бизнеса (FastAPI)

[![tests](https://github.com/your-username/business-crm-fastapi/actions/workflows/tests.yml/badge.svg)](https://github.com/your-username/business-crm-fastapi/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Postgres](https://img.shields.io/badge/PostgreSQL-16-336791)
![License](https://img.shields.io/badge/license-MIT-green)

Backend для CRM-системы малого бизнеса (салоны, барбершопы, студии, частные мастера):
учёт **клиентов**, **сотрудников**, **услуг** и **записей на приём**, ролевая модель
доступа, история действий и поиск/фильтрация. Проект построен по принципам **чистой
архитектуры** и готов к запуску одной командой через Docker.

> Это коммерческий pet-проект для портфолио: акцент на качестве кода, тестах,
> документации и инфраструктуре, а не на количестве фич.

---

## 📸 Скриншоты

| Swagger UI | Авторизация | Записи и фильтры |
|------------|-------------|------------------|
| ![Swagger](docs/screenshots/swagger.png) | ![Auth](docs/screenshots/auth.png) | ![Appointments](docs/screenshots/appointments.png) |

> Изображения — заглушки. Реальные скриншоты доступны после запуска на `http://localhost:8000/docs`.

---

## 🚀 Что демонстрирует проект

- **Чистая (слоистая) архитектура**: `api → services → repositories → models`, без утечки
  бизнес-логики в контроллеры и SQL — в сервисы.
- **FastAPI + Pydantic v2**: строгая валидация запросов/ответов, автогенерация
  Swagger/OpenAPI.
- **SQLAlchemy 2.0** (типизированные `Mapped`-модели) + **Alembic**-миграции.
- **JWT-авторизация** и **ролевая модель** доступа (`admin`, `manager`, `employee`) через
  переиспользуемые зависимости FastAPI.
- **Поиск и фильтрация**: по клиентам (имя/телефон/email), по записям (статус, даты,
  клиент, сотрудник), пагинация.
- **Аудит действий пользователей** (`activity_logs`).
- **Контейнеризация**: Docker + docker-compose (PostgreSQL, Redis, API) с автоматическим
  прогоном миграций при старте.
- **Тесты pytest** (16 тестов: авторизация, роли, CRUD, фильтрация, аудит) и **CI на
  GitHub Actions**.
- **Демо-данные (seed)** для мгновенного знакомства с API.

---

## 🧱 Стек

| Слой | Технологии |
|------|------------|
| Язык | Python 3.12 |
| Web | FastAPI, Uvicorn |
| Валидация | Pydantic v2, pydantic-settings |
| БД | PostgreSQL 16, SQLAlchemy 2.0 |
| Миграции | Alembic |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Кэш (опц.) | Redis |
| Тесты | pytest, httpx, TestClient |
| Инфра | Docker, docker-compose, GitHub Actions |

---

## 🏗️ Архитектура и структура

```
business-crm-fastapi/
├── app/
│   ├── api/            # HTTP-слой: роутеры FastAPI и зависимости (auth, роли)
│   │   ├── deps.py
│   │   └── v1/         # эндпоинты: auth, clients, employees, services, appointments, activity
│   ├── core/           # конфиг, безопасность (JWT/хэши), enum'ы
│   ├── db/             # подключение к БД, базовые классы, seed-данные
│   ├── models/         # ORM-модели SQLAlchemy 2.0
│   ├── schemas/        # Pydantic-схемы (DTO запросов/ответов)
│   ├── repositories/   # доступ к данным (запросы к БД)
│   ├── services/       # бизнес-логика
│   └── main.py         # точка входа FastAPI
├── alembic/            # миграции
├── tests/              # pytest
├── scripts/            # entrypoint для контейнера
├── docs/               # примеры запросов и скриншоты
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

**Принцип потока данных:** контроллер (`api`) принимает запрос → вызывает `service`
(бизнес-правила, проверки прав и связей) → `repository` выполняет операции с БД →
ORM-модель сохраняется → Pydantic-схема формирует ответ.

---

## ⚙️ Быстрый старт через Docker (рекомендуется)

```bash
# 1. Клонировать
git clone https://github.com/your-username/business-crm-fastapi.git
cd business-crm-fastapi

# 2. Подготовить переменные окружения
cp .env.example .env

# 3. Поднять стек (PostgreSQL + Redis + API)
docker compose up --build
```

При старте контейнер автоматически:
1. дожидается готовности PostgreSQL,
2. применяет миграции Alembic (`alembic upgrade head`),
3. загружает демо-данные (если `SEED_ON_STARTUP=true`),
4. запускает API.

Откройте документацию:
- **Swagger UI** — http://localhost:8000/docs
- **ReDoc** — http://localhost:8000/redoc
- **Health-check** — http://localhost:8000/health

### Демо-учётные записи (из seed)

| Роль | Email | Пароль |
|------|-------|--------|
| admin | `admin@crm.example.com` | `admin12345` |
| manager | `manager@crm.example.com` | `manager12345` |
| employee | `employee@crm.example.com` | `employee12345` |

---

## 💻 Локальный запуск без Docker

Нужен установленный PostgreSQL (или укажите `DATABASE_URL`).

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env                 # пропишите свои POSTGRES_* / DATABASE_URL

alembic upgrade head                 # миграции
python -m app.db.seed                # демо-данные (опционально)
uvicorn app.main:app --reload        # сервер на http://localhost:8000
```

---

## 🔐 Авторизация

1. Получите токен:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@crm.example.com","password":"admin12345"}'
   ```
2. Используйте его в заголовке: `Authorization: Bearer <token>`.
3. В Swagger UI нажмите **Authorize** и введите email/пароль (вкладка OAuth2).

### Матрица доступа

| Операция | admin | manager | employee |
|----------|:-----:|:-------:|:--------:|
| Просмотр клиентов/услуг/записей | ✅ | ✅ | ✅ |
| Создание/изменение клиентов и записей | ✅ | ✅ | ✅ |
| Удаление клиентов и записей | ✅ | ✅ | ❌ |
| Создание/изменение сотрудников и услуг | ✅ | ✅ | ❌ |
| Удаление сотрудников и услуг | ✅ | ❌ | ❌ |
| История действий (`/activity`) | ✅ | ✅ | ❌ |

---

## 📡 Примеры API-запросов

Полный набор — в [`docs/api-examples.http`](docs/api-examples.http).

```bash
# Создать клиента
curl -X POST http://localhost:8000/api/v1/clients \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"Анна Смирнова","phone":"+79001112233","email":"anna@example.com"}'

# Поиск клиентов
curl "http://localhost:8000/api/v1/clients?q=Анна" -H "Authorization: Bearer $TOKEN"

# Создать запись на приём
curl -X POST http://localhost:8000/api/v1/appointments \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"client_id":1,"employee_id":1,"service_id":1,"scheduled_at":"2026-07-01T10:00:00Z","status":"new"}'

# Фильтрация записей по статусу
curl "http://localhost:8000/api/v1/appointments?status=confirmed" -H "Authorization: Bearer $TOKEN"
```

### Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/api/v1/auth/register` | Регистрация |
| POST | `/api/v1/auth/login` | Логин (JSON) → JWT |
| GET | `/api/v1/auth/me` | Текущий пользователь |
| GET/POST/PATCH/DELETE | `/api/v1/clients` | CRUD + поиск клиентов |
| GET/POST/PATCH/DELETE | `/api/v1/employees` | CRUD сотрудников |
| GET/POST/PATCH/DELETE | `/api/v1/services` | CRUD услуг |
| GET/POST/PATCH/DELETE | `/api/v1/appointments` | CRUD + фильтрация записей |
| GET | `/api/v1/activity` | История действий |

---

## 🧪 Тесты

```bash
pytest -q
```

Тесты используют изолированную in-memory SQLite-базу (через переопределение зависимости
`get_db`), поэтому не требуют запущенного PostgreSQL. Покрытие: авторизация, роли,
CRUD клиентов, записи со связями, фильтрация по статусу, запись в журнал действий.

CI автоматически запускает миграции и тесты на каждый push/PR — см.
[`.github/workflows/tests.yml`](.github/workflows/tests.yml).

---

## 🗃️ Миграции (Alembic)

```bash
alembic upgrade head          # применить
alembic downgrade -1          # откатить на шаг
alembic revision --autogenerate -m "описание"   # создать новую миграцию
```

---

## 🛠️ Переменные окружения

См. [`.env.example`](.env.example). Ключевые:

| Переменная | Назначение |
|------------|------------|
| `SECRET_KEY` | секрет для подписи JWT (обязательно сменить в проде) |
| `POSTGRES_*` / `DATABASE_URL` | подключение к БД |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | срок жизни токена |
| `SEED_ON_STARTUP` | загружать ли демо-данные при старте |
| `REDIS_ENABLED` | включение Redis (опционально) |

---

## 📦 Публикация на GitHub

```bash
git init
git add .
git commit -m "feat: business-crm-fastapi — initial release"
git branch -M main
git remote add origin https://github.com/your-username/business-crm-fastapi.git
git push -u origin main
```

После пуша вкладка **Actions** покажет прохождение тестов, а бейдж в шапке README
станет активным. Не забудьте заменить `your-username` на свой GitHub-логин.

---

## 🧾 Текст для резюме

> **Business CRM (FastAPI) — backend CRM-системы для малого бизнеса.**
> Спроектировал и реализовал REST API на FastAPI с чистой слоистой архитектурой
> (api / services / repositories / models). Реализовал JWT-авторизацию и ролевую модель
> доступа (admin/manager/employee), CRUD клиентов, сотрудников, услуг и записей на приём,
> поиск и фильтрацию (по статусам, датам, контактам), а также журнал действий
> пользователей. Настроил PostgreSQL + SQLAlchemy 2.0, миграции Alembic, контейнеризацию
> через Docker Compose с автоприменением миграций, покрытие тестами на pytest и CI на
> GitHub Actions. Подготовил OpenAPI/Swagger-документацию и seed-данные для демонстрации.
>
> **Стек:** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, PostgreSQL, Alembic, JWT,
> Docker, pytest, GitHub Actions.

---

## 📄 Лицензия

MIT — используйте свободно в портфолио и коммерческих проектах.
