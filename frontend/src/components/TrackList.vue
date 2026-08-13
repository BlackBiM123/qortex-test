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
    class="track-list"
    handle=".drag-handle"
    @end="emit('reorder')"
  >
    <template #item="{ element }: { element: AlbumTrack }">
      <li class="track-row">
        <span class="drag-handle" title="Перетащите для изменения порядка">⠿</span>
        <span class="position">{{ element.position }}</span>
        <span class="song-title">{{ element.song.title }}</span>
        <button
          class="btn btn-danger remove-btn"
          type="button"
          title="Убрать из альбома"
          @click="emit('remove', element.id)"
        >
          ✕
        </button>
      </li>
    </template>
  </draggable>
</template>

<style scoped>
.track-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.track-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
}

.drag-handle {
  cursor: grab;
  color: var(--color-text-muted);
  user-select: none;
}

.position {
  width: 2ch;
  text-align: right;
  color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
}

.song-title {
  flex: 1;
}

.remove-btn {
  font-size: 0.75rem;
  padding: var(--space-1) var(--space-2);
}
</style>
