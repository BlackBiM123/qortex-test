<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useSongsStore } from '@/stores/songs'
import { useToast } from '@/composables/useToast'
import { useDebouncedRef } from '@/composables/useDebouncedRef'
import SearchInput from '@/components/SearchInput.vue'
import BasePagination from '@/components/BasePagination.vue'

const store = useSongsStore()
const toast = useToast()

const searchInput = ref('')
const debouncedSearch = useDebouncedRef('', 350)

watch(searchInput, (value) => {
  debouncedSearch.value = value
})

watch(debouncedSearch, (value) => {
  store.setSearch(value)
  store.fetchSongs()
})

function onPageChange(page: number) {
  store.setPage(page)
  store.fetchSongs()
}

async function handleDelete(id: number) {
  if (!confirm('Удалить песню из каталога?')) return
  try {
    await store.deleteSong(id)
    toast.success('Песня удалена.')
  } catch {
    toast.error('Не удалось удалить песню: она используется в одном или нескольких альбомах.')
  }
}

onMounted(() => store.fetchSongs())
</script>

<template>
  <div>
    <h1>Песни</h1>
    <p class="hint">
      Одна песня может входить в несколько альбомов под разными номерами трека — это видно в колонке
      «Используется в альбомах».
    </p>

    <SearchInput v-model="searchInput" placeholder="Поиск по названию…" />

    <p v-if="store.loading" class="state-message">Загрузка…</p>
    <p v-else-if="store.items.length === 0" class="state-message">Песни не найдены.</p>
    <ul v-else class="song-list">
      <li v-for="song in store.items" :key="song.id" class="song-row card">
        <div class="song-main">
          <span class="song-title">{{ song.title }}</span>
          <button class="btn btn-danger" type="button" @click="handleDelete(song.id)">
            Удалить
          </button>
        </div>
        <ul v-if="song.albums.length" class="album-usages">
          <li v-for="entry in song.albums" :key="entry.id">
            №{{ entry.position }} в
            <RouterLink :to="`/albums/${entry.album_id}`">
              «{{ entry.album_title }}» ({{ entry.artist_name }}, {{ entry.year }})
            </RouterLink>
          </li>
        </ul>
        <p v-else class="no-usage">Пока не входит ни в один альбом.</p>
      </li>
    </ul>

    <BasePagination
      :page="store.page"
      :total-pages="Math.max(1, Math.ceil(store.count / 20))"
      @update:page="onPageChange"
    />
  </div>
</template>

<style scoped>
h1 {
  margin: 0 0 var(--space-2);
  font-size: 1.5rem;
}

.hint {
  color: var(--color-text-muted);
  margin: 0 0 var(--space-5);
  font-size: 0.9375rem;
}

.song-list {
  list-style: none;
  margin: var(--space-5) 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.song-row {
  padding: var(--space-3) var(--space-4);
}

.song-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.song-title {
  font-weight: 500;
}

.album-usages {
  list-style: none;
  margin: var(--space-2) 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  font-size: 0.875rem;
  color: var(--color-text-muted);
}

.no-usage {
  margin: var(--space-2) 0 0;
  font-size: 0.875rem;
  color: var(--color-text-muted);
  font-style: italic;
}
</style>
