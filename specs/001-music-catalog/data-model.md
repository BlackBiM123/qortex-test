# Модель данных: Каталог музыкальных альбомов

Родитель: [spec.md](spec.md) · Реализация: `backend/catalog/models.py`

## ER-диаграмма

```
Artist (1) ──────< (N) Album (1) ──< (N) AlbumTrack (N) >── (1) Song
```

`AlbumTrack` — явная промежуточная (`through`) модель между `Album` и `Song`. Это единственный
способ выразить требование «песня входит в разные альбомы под разными номерами» без дублирования
записи песни.

## Сущности

### Artist
| Поле | Тип | Ограничения |
|---|---|---|
| `id` | PK | auto |
| `name` | `CharField(200)` | `unique=True`, индекс |

### Album
| Поле | Тип | Ограничения |
|---|---|---|
| `id` | PK | auto |
| `title` | `CharField(300)` | обязательное |
| `artist` | `FK(Artist)` | `on_delete=CASCADE`, `related_name="albums"` |
| `year` | `PositiveSmallIntegerField` | `1860 ≤ year ≤ текущий_год + 1` |

Ограничение: `UniqueConstraint(fields=["artist", "title", "year"], name="uniq_album_per_artist_year")`
— защита от случайных дублей одного и того же релиза.

### Song
| Поле | Тип | Ограничения |
|---|---|---|
| `id` | PK | auto |
| `title` | `CharField(300)` | обязательное, индекс (поиск) |

Намеренно **без** FK на альбом — песня существует независимо и может быть связана с 0..N альбомов.

### AlbumTrack (through-модель)
| Поле | Тип | Ограничения |
|---|---|---|
| `id` | PK | auto |
| `album` | `FK(Album)` | `on_delete=CASCADE`, `related_name="tracks"` |
| `song` | `FK(Song)` | `on_delete=PROTECT`, `related_name="track_entries"` |
| `position` | `PositiveSmallIntegerField` | `≥ 1` |

Ограничения БД:
- `UniqueConstraint(["album", "song"], name="uniq_song_per_album")` — FR-06: песня не может
  дважды входить в один альбом.
- `UniqueConstraint(["album", "position"], name="uniq_position_per_album", deferrable=Deferrable.DEFERRED)`
  — FR-07: номера треков внутри альбома не повторяются; `DEFERRED` позволяет переставить все
  позиции альбома одним батчем `UPDATE` внутри транзакции без промежуточного нарушения уникальности.

`on_delete=PROTECT` на `song` — реализация FR-08: удалить песню, у которой есть хотя бы одна
запись `AlbumTrack`, нельзя; Django поднимет `ProtectedError`, который API-слой превращает в
`409 Conflict` со списком альбомов, где песня используется.

## Инварианты (проверяются тестами `catalog/tests/test_models.py`)

1. **Переиспользование разрешено**: `Song` X в `Album` A с `position=1` и в `Album` B с
   `position=5` — валидное состояние (две записи `AlbumTrack`, одна `Song`).
2. **Дубль позиции запрещён**: второй `AlbumTrack` с тем же `(album, position)` → `IntegrityError`.
3. **Дубль песни в альбоме запрещён**: второй `AlbumTrack` с тем же `(album, song)` → `IntegrityError`.
4. **Защита песни от удаления**: `Song.delete()`, когда есть связанные `AlbumTrack`, → `ProtectedError`.
5. **Удаление альбома** каскадно удаляет его `AlbumTrack` (треклист), но не трогает сами `Song`.

## Примечание про SQLite

`Deferrable.DEFERRED` — особенность транзакционной модели PostgreSQL; SQLite её не поддерживает
(Django выводит system-check warning `models.W038` и ограничение применяется как обычное
`IMMEDIATE`). Это не критично для fallback-режима на SQLite, потому что операция reorder
(`POST /api/albums/{id}/tracks/reorder/`) реализована так, что не требует отложенной проверки:
сначала все выбранные треки переносятся во временный непересекающийся диапазон позиций
(`position + 1000`), затем — в целевые `1..N`, оба шага — в одной транзакции `atomic()`.
Основной путь запуска проекта (`docker compose up`) использует PostgreSQL, где ограничение
работает в полной, задуманной форме.
