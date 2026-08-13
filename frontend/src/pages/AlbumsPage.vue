<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAlbumsStore } from '@/stores/albums'
import { albumsApi } from '@/api/albums'
import { artistsApi } from '@/api/artists'
import { useToast } from '@/composables/useToast'
import { useDebouncedRef } from '@/composables/useDebouncedRef'
import type { Artist } from '@/types'
import SearchInput from '@/components/SearchInput.vue'
import AlbumCard from '@/components/AlbumCard.vue'
import BasePagination from '@/components/BasePagination.vue'
import BaseModal from '@/components/BaseModal.vue'
import AlbumForm from '@/components/AlbumForm.vue'

const store = useAlbumsStore()
const route = useRoute()
const router = useRouter()
const toast = useToast()

const artists = ref<Artist[]>([])
const searchInput = ref(store.filters.search)
const debouncedSearch = useDebouncedRef('', 350)
const showCreateModal = ref(false)
const submitting = ref(false)

watch(debouncedSearch, (value) => {
  store.setFilters({ search: value })
  syncQuery()
  store.fetchAlbums()
})

watch(searchInput, (value) => {
  debouncedSearch.value = value
})

function syncQuery() {
  router.replace({
    query: {
      search: store.filters.search || undefined,
      artist: store.filters.artist ?? undefined,
      year_min: store.filters.yearMin ?? undefined,
      year_max: store.filters.yearMax ?? undefined,
      page: store.page > 1 ? store.page : undefined,
    },
  })
}

function onArtistFilterChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value
  store.setFilters({ artist: value ? Number(value) : null })
  syncQuery()
  store.fetchAlbums()
}

function onYearMinChange(event: Event) {
  const value = (event.target as HTMLInputElement).value
  store.setFilters({ yearMin: value ? Number(value) : null })
  syncQuery()
  store.fetchAlbums()
}

function onYearMaxChange(event: Event) {
  const value = (event.target as HTMLInputElement).value
  store.setFilters({ yearMax: value ? Number(value) : null })
  syncQuery()
  store.fetchAlbums()
}

function onPageChange(page: number) {
  store.setPage(page)
  syncQuery()
  store.fetchAlbums()
}

async function handleDelete(id: number) {
  if (!confirm('Удалить альбом? Это действие необратимо.')) return
  try {
    await store.deleteAlbum(id)
    toast.success('Альбом удалён.')
  } catch {
    toast.error('Не удалось удалить альбом.')
  }
}

async function handleCreate(values: { title: string; artist: number; year: number }) {
  submitting.value = true
  try {
    await albumsApi.create(values)
    showCreateModal.value = false
    toast.success('Альбом создан.')
    await store.fetchAlbums()
  } catch {
    toast.error('Не удалось создать альбом. Проверьте данные.')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  const query = route.query
  store.filters.search = (query.search as string) ?? ''
  store.filters.artist = query.artist ? Number(query.artist) : null
  store.filters.yearMin = query.year_min ? Number(query.year_min) : null
  store.filters.yearMax = query.year_max ? Number(query.year_max) : null
  store.page = query.page ? Number(query.page) : 1
  searchInput.value = store.filters.search

  const [, artistsData] = await Promise.all([
    store.fetchAlbums(),
    artistsApi.list({ page: 1, page_size: 100 }).then((d) => d.results),
  ])
  artists.value = artistsData
})
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Альбомы</h1>
      <button class="btn btn-primary" type="button" @click="showCreateModal = true">
        + Добавить альбом
      </button>
    </div>

    <div class="filters">
      <SearchInput v-model="searchInput" placeholder="Поиск по названию или исполнителю…" />
      <select :value="store.filters.artist ?? ''" @change="onArtistFilterChange">
        <option value="">Все исполнители</option>
        <option v-for="artist in artists" :key="artist.id" :value="artist.id">
          {{ artist.name }}
        </option>
      </select>
      <input
        type="number"
        placeholder="Год от"
        :value="store.filters.yearMin ?? ''"
        @change="onYearMinChange"
      />
      <input
        type="number"
        placeholder="Год до"
        :value="store.filters.yearMax ?? ''"
        @change="onYearMaxChange"
      />
    </div>

    <p v-if="store.loading" class="state-message">Загрузка…</p>
    <p v-else-if="store.error" class="state-message">{{ store.error }}</p>
    <p v-else-if="store.items.length === 0" class="state-message">
      Ничего не найдено. Попробуйте изменить фильтры.
    </p>
    <div v-else class="albums-grid">
      <AlbumCard
        v-for="album in store.items"
        :key="album.id"
        :album="album"
        @delete="handleDelete"
      />
    </div>

    <BasePagination
      :page="store.page"
      :total-pages="store.totalPages"
      @update:page="onPageChange"
    />

    <BaseModal v-if="showCreateModal" title="Новый альбом" @close="showCreateModal = false">
      <AlbumForm :artists="artists" :submitting="submitting" @submit="handleCreate" />
    </BaseModal>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-5);
  gap: var(--space-3);
  flex-wrap: wrap;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.filters {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.filters select,
.filters input[type='number'] {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text);
}

.albums-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: var(--space-4);
}

@media (max-width: 640px) {
  .filters {
    grid-template-columns: 1fr;
  }
}
</style>
