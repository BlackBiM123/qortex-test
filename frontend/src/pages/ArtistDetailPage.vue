<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { artistsApi } from '@/api/artists'
import { albumsApi } from '@/api/albums'
import type { AlbumListItem, Artist } from '@/types'

const props = defineProps<{ id: string }>()
const router = useRouter()

const artist = ref<Artist | null>(null)
const albums = ref<AlbumListItem[]>([])
const loading = ref(true)
const artistId = computed(() => Number(props.id))

onMounted(async () => {
  loading.value = true
  try {
    const [artistData, albumsData] = await Promise.all([
      artistsApi.get(artistId.value),
      albumsApi.list({ artist: artistId.value, page_size: 100 }),
    ])
    artist.value = artistData
    albums.value = albumsData.results
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <button
      type="button"
      class="mb-8 font-mono text-xs tracking-widest text-ink-muted uppercase hover:text-accent"
      @click="router.push('/artists')"
    >
      ← К исполнителям
    </button>

    <p v-if="loading" class="py-16 text-center font-mono text-sm text-ink-muted">Загрузка…</p>
    <template v-else-if="artist">
      <h1 class="font-display text-4xl font-bold tracking-tight text-ink">{{ artist.name }}</h1>
      <p class="mt-2 font-mono text-sm tabular-nums text-ink-muted">
        {{ artist.albums_count }} альбомов в каталоге
      </p>

      <ul v-if="albums.length" class="mt-6 flex flex-col border border-line bg-surface">
        <li
          v-for="album in albums"
          :key="album.id"
          class="flex items-center justify-between gap-4 border-b border-line px-4 py-3 last:border-b-0"
        >
          <RouterLink
            :to="`/albums/${album.id}`"
            class="font-medium text-ink no-underline hover:text-accent hover:no-underline"
            >{{ album.title }}</RouterLink
          >
          <span class="font-mono text-xs tabular-nums text-ink-muted"
            >{{ album.year }} · {{ album.tracks_count }} треков</span
          >
        </li>
      </ul>
      <p v-else class="py-16 text-center font-mono text-sm text-ink-muted">
        У этого исполнителя пока нет альбомов.
      </p>
    </template>
  </div>
</template>
