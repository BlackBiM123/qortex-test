# Каталог музыкальных альбомов

Веб-приложение для каталогизации музыкальных альбомов: исполнители, альбомы, песни и треклисты.
Ключевая особенность предметной области — **одна и та же песня может входить в разные альбомы
под разными порядковыми номерами** (например, концертная версия или переиздание).

Тестовое задание для позиции Fullstack-разработчик (Vue, Django), выполненное по принципам
**Spec-Driven Development**: сначала спецификация и план (см. [`specs/`](specs/)), затем код.

## Стек

- **Backend**: Python 3.13, Django 6.1, Django REST Framework, PostgreSQL 17, drf-spectacular.
- **Frontend**: Vue 3 (Composition API, `<script setup>`, TypeScript), Vite, Pinia, Vue Router,
  axios, vuedraggable (drag&drop треклиста).
- **Тесты**: pytest + pytest-django + factory-boy (backend), Vitest + @vue/test-utils (frontend).
- **Инфраструктура**: Docker Compose, GitHub Actions CI.

## Быстрый старт (Docker Compose)

Требуется Docker Desktop.

```bash
git clone https://github.com/BlackBiM123/qortex-test.git
cd qortex-test
cp .env.example .env
docker compose up --build
```

После запуска:

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000/api/
- **Swagger UI**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/ (нужно создать суперпользователя, см. ниже)

При первом запуске backend автоматически применяет миграции и наполняет базу демоданными
(`seed_demo`), в которых песня **«Money»** намеренно входит сразу в три альбома с разными
номерами трека — это готовый пример ключевого сценария ТЗ, который можно сразу открыть на
странице «Песни».

Создать администратора для Django Admin:

```bash
docker compose exec backend python manage.py createsuperuser
```

Остановить и удалить контейнеры (данные в volume `db_data` сохранятся):

```bash
docker compose down
```

Полная остановка с удалением данных:

```bash
docker compose down -v
```

## Локальный запуск без Docker (SQLite)

Backend (требуется Python 3.12+ и [uv](https://docs.astral.sh/uv/)):

```bash
cd backend
uv sync --group dev
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

Frontend (требуется Node.js 20+, в отдельном терминале):

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на http://localhost:5173 и проксировать `/api` на
`http://localhost:8000` (см. `frontend/vite.config.ts`).

> На SQLite одно из ограничений целостности (`uniq_position_per_album`) создаётся в упрощённом
> виде — Django выводит предупреждение `models.W038` при `migrate`. Подробности и почему это
> не влияет на корректность работы — в [`specs/001-music-catalog/data-model.md`](specs/001-music-catalog/data-model.md#примечание-про-sqlite).

## Тесты и линтеры

Backend:

```bash
cd backend
uv run pytest              # тесты
uv run ruff check .        # линт
uv run ruff format --check .  # форматирование
```

Через Docker:

```bash
docker compose exec backend uv run pytest
```

Frontend:

```bash
cd frontend
npm run test        # Vitest
npm run lint         # ESLint
npm run typecheck    # vue-tsc --noEmit
npm run build         # production-сборка
```

CI (`.github/workflows/ci.yml`) прогоняет всё это на каждый push/PR — backend-тесты идут
против настоящего PostgreSQL, а не SQLite.

## Структура репозитория

```
├── specs/                    # SDD-документы: constitution, spec, plan, data-model, tasks, OpenAPI
├── backend/                  # Django + DRF
│   └── catalog/              # приложение: модели, API, тесты
├── frontend/                 # Vue 3 + Vite SPA
│   └── src/
│       ├── api/              # HTTP-слой
│       ├── stores/           # Pinia (бизнес-состояние, без HTTP-деталей)
│       ├── components/       # переиспользуемые компоненты
│       └── pages/            # страницы-маршруты
├── compose.yaml               # docker compose (db / backend / frontend)
└── .github/workflows/ci.yml   # CI
```

## Модель данных

```
Artist (1) ──< Album (1) ──< AlbumTrack >── (1) Song
```

`AlbumTrack` — явная промежуточная модель между `Album` и `Song`, несущая порядковый номер
трека (`position`). Именно это позволяет одной песне входить в разные альбомы под разными
номерами — прямая связь `Song → Album` для этого не подходит, так как привязала бы песню
к одному-единственному альбому.

Полное описание сущностей, ограничений БД и инвариантов — в
[`specs/001-music-catalog/data-model.md`](specs/001-music-catalog/data-model.md).

## API

Основные эндпоинты (полная спецификация — `/api/schema/`, интерактивная документация —
`/api/docs/`):

| Метод | Путь | Назначение |
|---|---|---|
| `GET/POST` | `/api/artists/` | список / создание исполнителей |
| `GET/POST` | `/api/albums/` | список (поиск, фильтры, пагинация) / создание альбомов |
| `GET/PATCH/DELETE` | `/api/albums/{id}/` | альбом с полным треклистом |
| `POST` | `/api/albums/{id}/tracks/` | добавить трек (`song_id` существующей песни **или** `song_title` новой) |
| `PATCH/DELETE` | `/api/albums/{id}/tracks/{track_id}/` | изменить позицию / убрать трек из альбома |
| `POST` | `/api/albums/{id}/tracks/reorder/` | атомарная перенумерация треков по новому порядку |
| `GET/POST` | `/api/songs/` | список / создание песен |
| `GET` | `/api/songs/{id}/` | песня со списком всех альбомов, где используется, и номером в каждом |

Готовый OpenAPI-контракт (экспортирован из drf-spectacular): [`specs/001-music-catalog/contracts/openapi.yaml`](specs/001-music-catalog/contracts/openapi.yaml).

## Архитектурные решения

Кратко (подробное обоснование — в [`specs/001-music-catalog/plan.md`](specs/001-music-catalog/plan.md)):

- **M2M через `through`-модель**, а не `ForeignKey` от песни к альбому — единственный способ
  корректно смоделировать переиспользование песни (ключевое требование ТЗ).
- **Ограничения целостности — на уровне БД** (`UniqueConstraint`), а не только в коде: защита
  от гонок и от прямых изменений в обход API.
- **`on_delete=PROTECT`** на связи трека с песней — нельзя удалить песню, которая используется
  хотя бы в одном альбоме; API возвращает `409` со списком альбомов.
- **Разделение слоёв на фронтенде**: `api/` (HTTP) → `stores/` (Pinia, бизнес-состояние) →
  компоненты. Компоненты никогда не вызывают HTTP напрямую.
- **Аутентификация сознательно не реализована** — вне объёма тестового задания (см.
  `specs/001-music-catalog/spec.md`, раздел Non-Goals).

## Процесс разработки (SDD)

История коммитов отражает порядок Spec-Driven Development: сначала `specs/` (constitution →
spec → plan → data-model → tasks), затем реализация backend, frontend, инфраструктуры и CI —
каждый коммит реализации ссылается на номер задачи из
[`specs/001-music-catalog/tasks.md`](specs/001-music-catalog/tasks.md).
