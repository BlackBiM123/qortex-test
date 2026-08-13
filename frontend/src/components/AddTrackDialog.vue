<script setup lang="ts">
import { ref, watch } from 'vue'
import { songsApi } from '@/api/songs'
import { useDebouncedRef } from '@/composables/useDebouncedRef'
import type { SongLite } from '@/types'
import type { AddTrackData } from '@/api/albums'

const props = defineProps<{ submitting?: boolean }>()
const emit = defineEmits<{ submit: [data: AddTrackData] }>()

type Mode = 'existing' | 'new'
const mode = ref<Mode>('existing')

const query = ref('')
const debouncedQuery = useDebouncedRef('', 300)
const results = ref<SongLite[]>([])
const selectedSong = ref<SongLite | null>(null)

const newTitle = ref('')
const position = ref<number | null>(null)

watch(query, (value) => {
  debouncedQuery.value = value
})

watch(debouncedQuery, async (value) => {
  if (!value.trim()) {
    results.value = []
    return
  }
  results.value = await songsApi.search(value.trim())
})

function pickSong(song: SongLite) {
  selectedSong.value = song
  query.value = song.title
  results.value = []
}

function handleSubmit() {
  const data: AddTrackData = {}
  if (position.value) data.position = position.value

  if (mode.value === 'existing') {
    if (!selectedSong.value) return
    data.song_id = selectedSong.value.id
  } else {
    if (!newTitle.value.trim()) return
    data.song_title = newTitle.value.trim()
  }
  emit('submit', data)
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="mode-tabs">
      <button
        type="button"
        class="btn"
        :class="mode === 'existing' ? 'btn-primary' : 'btn-secondary'"
        @click="mode = 'existing'"
      >
        Существующая песня
      </button>
      <button
        type="button"
        class="btn"
        :class="mode === 'new' ? 'btn-primary' : 'btn-secondary'"
        @click="mode = 'new'"
      >
        Новая песня
      </button>
    </div>

    <div v-if="mode === 'existing'" class="field autocomplete">
      <label for="song-search">Найдите песню в каталоге</label>
      <input
        id="song-search"
        v-model="query"
        type="text"
        autocomplete="off"
        placeholder="Начните вводить название…"
        @input="selectedSong = null"
      />
      <ul v-if="results.length" class="results">
        <li v-for="song in results" :key="song.id" @click="pickSong(song)">
          {{ song.title }}
        </li>
      </ul>
      <span v-if="selectedSong" class="field-hint">Выбрано: «{{ selectedSong.title }}»</span>
    </div>

    <div v-else class="field">
      <label for="new-song-title">Название новой песни</label>
      <input id="new-song-title" v-model="newTitle" type="text" autocomplete="off" />
    </div>

    <div class="field">
      <label for="track-position">Номер трека (необязательно)</label>
      <input id="track-position" v-model.number="position" type="number" min="1" />
    </div>

    <button
      class="btn btn-primary"
      type="submit"
      :disabled="props.submitting || (mode === 'existing' ? !selectedSong : !newTitle.trim())"
    >
      {{ props.submitting ? 'Добавление…' : 'Добавить трек' }}
    </button>
  </form>
</template>

<style scoped>
.mode-tabs {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.autocomplete {
  position: relative;
}

.results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 10;
  list-style: none;
  margin: 0;
  padding: var(--space-1) 0;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  max-height: 200px;
  overflow-y: auto;
}

.results li {
  padding: var(--space-2) var(--space-3);
  cursor: pointer;
}

.results li:hover {
  background: var(--color-bg);
}

.field-hint {
  font-size: 0.8125rem;
  color: var(--color-success);
}
</style>
