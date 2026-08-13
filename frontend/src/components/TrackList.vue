<script setup lang="ts">
import draggable from 'vuedraggable'
import type { AlbumTrack } from '@/types'

const model = defineModel<AlbumTrack[]>({ required: true })
const emit = defineEmits<{ reorder: []; remove: [trackId: number] }>()
</script>

<template>
  <draggable
    v-model="model"
    item-key="id"
    tag="ol"
    class="border border-line bg-surface"
    handle=".drag-handle"
    @end="emit('reorder')"
  >
    <template #item="{ element }: { element: AlbumTrack }">
      <li
        class="track-row group flex items-center gap-4 border-b border-line px-4 py-3 last:border-b-0"
      >
        <span
          class="drag-handle cursor-grab font-mono text-ink-faint select-none"
          title="Перетащите для изменения порядка"
          >⠿</span
        >
        <span class="w-6 text-right font-mono text-sm tabular-nums text-gold">{{
          element.position
        }}</span>
        <span class="flex-1 text-ink">{{ element.song.title }}</span>
        <button
          type="button"
          title="Убрать из альбома"
          class="remove-btn font-mono text-xs text-danger opacity-0 transition-opacity group-hover:opacity-100 hover:underline"
          @click="emit('remove', element.id)"
        >
          Убрать
        </button>
      </li>
    </template>
  </draggable>
</template>
