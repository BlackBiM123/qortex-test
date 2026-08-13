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
    <button class="btn btn-secondary back-btn" type="button" @click="router.push('/')">
      ← К списку альбомов
    </button>

    <p v-if="store.loading" class="state-message">Загрузка…</p>
    <p v-else-if="store.error && !store.album" class="state-message">{{ store.error }}</p>

    <template v-else-if="store.album">
      <div class="album-header">
        <h1>{{ store.album.title }}</h1>
        <p class="artist">{{ store.album.artist_name }} · {{ store.album.year }}</p>
      </div>

      <div class="tracks-section">
        <div class="tracks-header">
          <h2>Треки</h2>
          <button class="btn btn-primary" type="button" @click="showAddModal = true">
            + Добавить трек
          </button>
        </div>

        <p v-if="localTracks.length === 0" class="state-message">В альбоме пока нет треков.</p>
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

<style scoped>
.back-btn {
  margin-bottom: var(--space-5);
}

.album-header h1 {
  margin: 0 0 var(--space-1);
  font-size: 1.75rem;
}

.artist {
  margin: 0;
  color: var(--color-text-muted);
}

.tracks-section {
  margin-top: var(--space-6);
}

.tracks-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
}

.tracks-header h2 {
  margin: 0;
  font-size: 1.25rem;
}
</style>
