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
    <h1 class="font-display text-3xl font-bold tracking-tight text-ink">Песни</h1>
    <p class="mt-2 mb-8 max-w-2xl text-sm text-ink-muted">
      Одна песня может входить в несколько альбомов под разными номерами трека — это видно в колонке
      «Используется в альбомах».
    </p>

    <SearchInput v-model="searchInput" placeholder="Поиск по названию…" />

    <p v-if="store.loading" class="py-16 text-center font-mono text-sm text-ink-muted">Загрузка…</p>
    <p
      v-else-if="store.items.length === 0"
      class="py-16 text-center font-mono text-sm text-ink-muted"
    >
      Песни не найдены.
    </p>
    <ul v-else class="mt-6 flex flex-col gap-3">
      <li v-for="song in store.items" :key="song.id" class="border border-line bg-surface p-4">
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="font-medium text-ink">{{ song.title }}</span>
            <span
              v-if="song.albums.length > 1"
              class="border border-gold px-1.5 py-0.5 font-mono text-[0.65rem] tracking-widest text-gold uppercase"
              >{{ song.albums.length }} альбома</span
            >
          </div>
          <button
            type="button"
            class="font-mono text-xs text-danger hover:underline"
            @click="handleDelete(song.id)"
          >
            Удалить
          </button>
        </div>
        <ul v-if="song.albums.length" class="mt-3 flex flex-col gap-1.5 border-t border-line pt-3">
          <li
            v-for="entry in song.albums"
            :key="entry.id"
            class="flex items-baseline gap-2 text-sm"
          >
            <span class="w-6 shrink-0 font-mono text-xs tabular-nums text-gold"
              >№{{ entry.position }}</span
            >
            <RouterLink :to="`/albums/${entry.album_id}`" class="text-ink-muted hover:text-accent">
              «{{ entry.album_title }}» ({{ entry.artist_name }}, {{ entry.year }})
            </RouterLink>
          </li>
        </ul>
        <p v-else class="mt-3 border-t border-line pt-3 text-sm text-ink-faint italic">
          Пока не входит ни в один альбом.
        </p>
      </li>
    </ul>

    <BasePagination
      :page="store.page"
      :total-pages="Math.max(1, Math.ceil(store.count / 20))"
      @update:page="onPageChange"
    />
  </div>
</template>
