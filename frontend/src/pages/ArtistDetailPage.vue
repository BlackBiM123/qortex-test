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
    <button class="btn btn-secondary back-btn" type="button" @click="router.push('/artists')">
      ← К исполнителям
    </button>

    <p v-if="loading" class="state-message">Загрузка…</p>
    <template v-else-if="artist">
      <h1>{{ artist.name }}</h1>
      <p class="meta">{{ artist.albums_count }} альбомов в каталоге</p>

      <ul v-if="albums.length" class="album-list">
        <li v-for="album in albums" :key="album.id" class="card album-row">
          <RouterLink :to="`/albums/${album.id}`">{{ album.title }}</RouterLink>
          <span class="meta">{{ album.year }} · {{ album.tracks_count }} треков</span>
        </li>
      </ul>
      <p v-else class="state-message">У этого исполнителя пока нет альбомов.</p>
    </template>
  </div>
</template>

<style scoped>
.back-btn {
  margin-bottom: var(--space-5);
}

.meta {
  color: var(--color-text-muted);
  font-size: 0.9375rem;
}

.album-list {
  list-style: none;
  margin: var(--space-5) 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.album-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
}
</style>
