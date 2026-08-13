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
  <form class="flex flex-col gap-5" @submit.prevent="handleSubmit">
    <div class="flex border border-line font-mono text-xs tracking-widest uppercase">
      <button
        type="button"
        class="flex-1 px-3 py-2 transition-colors"
        :class="
          mode === 'existing' ? 'bg-ink text-paper' : 'bg-surface text-ink-muted hover:text-ink'
        "
        @click="mode = 'existing'"
      >
        Существующая песня
      </button>
      <button
        type="button"
        class="flex-1 px-3 py-2 transition-colors"
        :class="mode === 'new' ? 'bg-ink text-paper' : 'bg-surface text-ink-muted hover:text-ink'"
        @click="mode = 'new'"
      >
        Новая песня
      </button>
    </div>

    <div v-if="mode === 'existing'" class="relative">
      <label
        for="song-search"
        class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
        >Найдите песню в каталоге</label
      >
      <input
        id="song-search"
        v-model="query"
        type="text"
        autocomplete="off"
        placeholder="Начните вводить название…"
        class="w-full border border-line bg-surface px-3 py-2 text-ink focus-visible:border-accent"
        @input="selectedSong = null"
      />
      <ul
        v-if="results.length"
        class="absolute inset-x-0 top-full z-10 max-h-48 overflow-y-auto border border-t-0 border-line bg-surface shadow-lg"
      >
        <li
          v-for="song in results"
          :key="song.id"
          class="cursor-pointer px-3 py-2 text-ink hover:bg-paper"
          @click="pickSong(song)"
        >
          {{ song.title }}
        </li>
      </ul>
      <span v-if="selectedSong" class="mt-1 block text-xs text-success"
        >Выбрано: «{{ selectedSong.title }}»</span
      >
    </div>

    <div v-else>
      <label
        for="new-song-title"
        class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
        >Название новой песни</label
      >
      <input
        id="new-song-title"
        v-model="newTitle"
        type="text"
        autocomplete="off"
        class="w-full border border-line bg-surface px-3 py-2 text-ink focus-visible:border-accent"
      />
    </div>

    <div>
      <label
        for="track-position"
        class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
        >Номер трека (необязательно)</label
      >
      <input
        id="track-position"
        v-model.number="position"
        type="number"
        min="1"
        class="w-full border border-line bg-surface px-3 py-2 font-mono tabular-nums text-ink focus-visible:border-accent"
      />
    </div>

    <button
      type="submit"
      :disabled="props.submitting || (mode === 'existing' ? !selectedSong : !newTitle.trim())"
      class="self-start bg-accent px-5 py-2.5 font-mono text-xs tracking-widest text-paper uppercase transition-colors hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-40"
    >
      {{ props.submitting ? 'Добавление…' : 'Добавить трек' }}
    </button>
  </form>
</template>
