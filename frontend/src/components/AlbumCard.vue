<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { AlbumListItem } from '@/types'

defineProps<{ album: AlbumListItem }>()
defineEmits<{ delete: [id: number] }>()
</script>

<template>
  <div class="group flex border border-line bg-surface transition-shadow hover:shadow-md">
    <!-- Корешок: как у пластинки на полке. -->
    <div class="w-2 shrink-0 bg-accent transition-colors group-hover:bg-gold" />

    <div class="flex flex-1 flex-col gap-3 p-4">
      <RouterLink :to="`/albums/${album.id}`" class="no-underline hover:no-underline">
        <h3 class="font-display text-lg leading-tight font-semibold text-ink">
          {{ album.title }}
        </h3>
        <p class="mt-1 text-sm text-ink-muted">{{ album.artist_name }}</p>
      </RouterLink>

      <div
        class="mt-auto flex items-center justify-between border-t border-line pt-3 font-mono text-xs text-ink-faint"
      >
        <span class="tabular-nums">{{ album.year }}</span>
        <span class="tabular-nums">{{ album.tracks_count }} треков</span>
      </div>

      <button
        type="button"
        title="Удалить альбом"
        class="self-start font-mono text-xs text-danger opacity-0 transition-opacity group-hover:opacity-100 hover:underline"
        @click="$emit('delete', album.id)"
      >
        Удалить
      </button>
    </div>
  </div>
</template>
