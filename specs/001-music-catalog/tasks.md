# Задачи: Каталог музыкальных альбомов

Каждая задача трассируется на функциональные требования из [spec.md](spec.md).
Статус обновляется по мере реализации; коммит реализации ссылается на T-id.

## Backend

| ID | Задача | Трассировка | Статус |
|---|---|---|---|
| T-01 | Инициализация Django-проекта (`config`), приложение `catalog`, настройки dev/prod | — | ✅ |
| T-02 | Модели `Artist`, `Album`, `Song`, `AlbumTrack` с ограничениями БД | FR-01…FR-08 | ✅ |
| T-03 | Миграции, регистрация в Django Admin | FR-13 | ✅ |
| T-04 | Сериализаторы (List/Detail для Album), кастомный exception handler | FR-15 | ✅ |
| T-05 | ViewSets `Artist`, `Album`, `Song` + роутер | FR-13 | ✅ |
| T-06 | Actions треков: добавить / изменить / удалить трек альбома | FR-04, FR-06, FR-07, FR-09 | ✅ |
| T-07 | Action `reorder` треков альбома (атомарная перенумерация) | FR-10 | ✅ |
| T-08 | Фильтры (artist, year, year_min/max), поиск, пагинация | FR-11, FR-12 | ✅ |
| T-09 | drf-spectacular, экспорт `contracts/openapi.yaml` | FR-14 | ✅ |
| T-10 | `seed_demo` management command | AC-1 (демонстрация) | ✅ |
| T-11 | Тесты моделей (инварианты 1-5 из data-model.md) | FR-05…FR-08 | ✅ |
| T-12 | Тесты API: CRUD, AC-1…AC-7 | все AC | ✅ |
| T-13 | Тест на отсутствие N+1 (assertNumQueries) | производительность (constitution §3) | ✅ |
| T-14 | ruff (lint + format) конфигурация | constitution §4 | ✅ |

## Frontend

| ID | Задача | Трассировка | Статус |
|---|---|---|---|
| T-15 | Инициализация Vite + Vue3 + TS проекта, роутинг | — | ✅ |
| T-16 | Типы DTO (`src/types`), API-клиент (`src/api`) | FR-13 | ✅ |
| T-17 | Pinia store альбомов (список, фильтры, пагинация, query-sync) | FR-11 | ✅ |
| T-18 | Pinia store исполнителей и песен | FR-01, FR-03, FR-12 | ✅ |
| T-19 | AlbumsPage: карточки, поиск, фильтры, пагинация | FR-11, US-5 | ✅ |
| T-20 | AlbumForm (создание/редактирование альбома) | FR-02, FR-13 | ✅ |
| T-21 | AlbumDetailPage + TrackList с drag&drop | US-4, FR-10 | ✅ |
| T-22 | AddTrackDialog (выбор существующей песни ИЛИ создание новой) | FR-09, US-2, US-3 | ✅ |
| T-23 | ArtistsPage / ArtistDetailPage | FR-01, FR-13 | ✅ |
| T-24 | SongsPage с отображением «входит в альбомы» | FR-12, US-6, AC-7 | ✅ |
| T-25 | Общие компоненты (BaseModal, BasePagination, SearchInput, AppToast) | — | ✅ |
| T-26 | ESLint + Prettier конфигурация, vue-tsc | constitution §4 | ✅ |

## Тесты

| ID | Задача | Трассировка | Статус |
|---|---|---|---|
| T-27 | Vitest: store albums (фильтры, пагинация, моки api) | FR-11 | ✅ |
| T-28 | Vitest: TrackList reorder + откат при ошибке | US-4 | ✅ |
| T-29 | Vitest: AlbumForm валидация года/обязательных полей | FR-02 | ✅ |

## Инфраструктура

| ID | Задача | Трассировка | Статус |
|---|---|---|---|
| T-30 | Dockerfile backend (uv, python:3.13-slim) | constitution §6 | ✅ |
| T-31 | Dockerfile frontend (node:24-alpine) | constitution §6 | ✅ |
| T-32 | `compose.yaml` (db/backend/frontend), `.env.example` | constitution §6 | ✅ |
| T-33 | GitHub Actions CI (backend + frontend jobs) | constitution §4 | ✅ |
| T-34 | README.md (запуск, API, архитектурные решения) | constitution §6 | ✅ |

## Итог

Все задачи трассируются на конкретные FR/AC/US из `spec.md`. Задач, не привязанных к
требованию, в этом списке нет — если бы появилась такая необходимость, сначала правится
`spec.md` (см. constitution.md §1).
