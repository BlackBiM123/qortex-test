<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { AlbumListItem } from '@/types'

defineProps<{ album: AlbumListItem }>()
defineEmits<{ delete: [id: number] }>()
</script>

<template>
  <div class="album-card card">
    <RouterLink :to="`/albums/${album.id}`" class="album-link">
      <h3>{{ album.title }}</h3>
      <p class="artist">{{ album.artist_name }}</p>
      <p class="meta">{{ album.year }} · {{ album.tracks_count }} треков</p>
    </RouterLink>
    <button
      class="btn btn-danger delete-btn"
      type="button"
      title="Удалить альбом"
      @click="$emit('delete', album.id)"
    >
      Удалить
    </button>
  </div>
</template>

<style scoped>
.album-card {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  transition: box-shadow 0.15s;
}

.album-card:hover {
  box-shadow: var(--shadow-md);
}

.album-link {
  color: var(--color-text);
  flex: 1;
}

.album-link:hover {
  text-decoration: none;
}

.album-link h3 {
  margin: 0 0 var(--space-1);
  font-size: 1.0625rem;
}

.artist {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 0.9375rem;
}

.meta {
  margin: var(--space-1) 0 0;
  color: var(--color-text-muted);
  font-size: 0.8125rem;
}

.delete-btn {
  align-self: flex-start;
  font-size: 0.8125rem;
  padding: var(--space-1) var(--space-2);
}
</style>
