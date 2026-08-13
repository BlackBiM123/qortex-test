<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAlbumDetailStore } from '@/stores/albumDetail'
import { useToast } from '@/composables/useToast'
import type { AlbumTrack } from '@/types'
import type { AddTrackData } from '@/api/albums'
import TrackList from '@/components/TrackList.vue'
import BaseModal from '@/components/BaseModal.vue'
import AddTrackDialog from '@/components/AddTrackDialog.vue'

const props = defineProps<{ id: string }>()
const store = useAlbumDetailStore()
const router = useRouter()
const toast = useToast()

const albumId = computed(() => Number(props.id))
const showAddModal = ref(false)
const addingTrack = ref(false)

const localTracks = computed<AlbumTrack[]>({
  get: () => store.album?.tracks ?? [],
  set: (value) => {
    if (store.album) store.album.tracks = value
  },
})

async function handleReorder() {
  try {
    await store.reorderTracks(localTracks.value)
  } catch {
    toast.error('Не удалось сохранить новый порядок треков. Изменения отменены.')
  }
}

async function handleRemoveTrack(trackId: number) {
  if (!confirm('Убрать эту песню из альбома?')) return
  try {
    await store.removeTrack(trackId)
    toast.success('Трек удалён из альбома.')
  } catch {
    toast.error('Не удалось удалить трек.')
  }
}

async function handleAddTrack(data: AddTrackData) {
  addingTrack.value = true
  try {
    await store.addTrack(data)
    showAddModal.value = false
    toast.success('Трек добавлен в альбом.')
  } catch {
    toast.error('Не удалось добавить трек: возможно, такая песня или номер уже заняты.')
  } finally {
    addingTrack.value = false
  }
}

onMounted(() => {
  store.fetchAlbum(albumId.value)
})
</script>

<template>
  <div>
    <button
      type="button"
      class="mb-8 font-mono text-xs tracking-widest text-ink-muted uppercase hover:text-accent"
      @click="router.push('/')"
    >
      ← К списку альбомов
    </button>

    <p v-if="store.loading" class="py-16 text-center font-mono text-sm text-ink-muted">Загрузка…</p>
    <p
      v-else-if="store.error && !store.album"
      class="py-16 text-center font-mono text-sm text-danger"
    >
      {{ store.error }}
    </p>

    <template v-else-if="store.album">
      <div class="mb-10 border-b-2 border-ink pb-6">
        <h1 class="font-display text-4xl font-bold tracking-tight text-ink">
          {{ store.album.title }}
        </h1>
        <p class="mt-2 font-mono text-sm text-ink-muted">
          {{ store.album.artist_name }} <span class="text-ink-faint">·</span>
          <span class="tabular-nums">{{ store.album.year }}</span>
        </p>
      </div>

      <div>
        <div class="mb-4 flex items-center justify-between">
          <h2 class="font-display text-xl font-semibold tracking-tight text-ink uppercase">
            Треки
          </h2>
          <button
            type="button"
            class="border border-ink px-4 py-2 font-mono text-xs tracking-widest text-ink uppercase transition-colors hover:bg-ink hover:text-paper"
            @click="showAddModal = true"
          >
            + Добавить трек
          </button>
        </div>

        <p
          v-if="localTracks.length === 0"
          class="py-10 text-center font-mono text-sm text-ink-muted"
        >
          В альбоме пока нет треков.
        </p>
        <TrackList
          v-else
          v-model="localTracks"
          @reorder="handleReorder"
          @remove="handleRemoveTrack"
        />
      </div>
    </template>

    <BaseModal v-if="showAddModal" title="Добавить трек" @close="showAddModal = false">
      <AddTrackDialog :submitting="addingTrack" @submit="handleAddTrack" />
    </BaseModal>
  </div>
</template>
