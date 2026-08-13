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
    <div class="mb-8 flex flex-wrap items-baseline justify-between gap-3">
      <h1 class="font-display text-3xl font-bold tracking-tight text-ink">Альбомы</h1>
      <button
        type="button"
        class="border border-ink px-4 py-2 font-mono text-xs tracking-widest text-ink uppercase transition-colors hover:bg-ink hover:text-paper"
        @click="showCreateModal = true"
      >
        + Добавить альбом
      </button>
    </div>

    <div
      class="mb-8 grid grid-cols-1 gap-3 border border-line bg-surface p-4 sm:grid-cols-2 lg:grid-cols-4"
    >
      <SearchInput v-model="searchInput" placeholder="Поиск по названию или исполнителю…" />
      <select
        :value="store.filters.artist ?? ''"
        class="border border-line bg-surface px-3 py-2 text-ink focus-visible:border-accent"
        @change="onArtistFilterChange"
      >
        <option value="">Все исполнители</option>
        <option v-for="artist in artists" :key="artist.id" :value="artist.id">
          {{ artist.name }}
        </option>
      </select>
      <input
        type="number"
        placeholder="Год от"
        :value="store.filters.yearMin ?? ''"
        class="border border-line bg-surface px-3 py-2 font-mono tabular-nums text-ink placeholder:font-sans focus-visible:border-accent"
        @change="onYearMinChange"
      />
      <input
        type="number"
        placeholder="Год до"
        :value="store.filters.yearMax ?? ''"
        class="border border-line bg-surface px-3 py-2 font-mono tabular-nums text-ink placeholder:font-sans focus-visible:border-accent"
        @change="onYearMaxChange"
      />
    </div>

    <p v-if="store.loading" class="py-16 text-center font-mono text-sm text-ink-muted">Загрузка…</p>
    <p v-else-if="store.error" class="py-16 text-center font-mono text-sm text-danger">
      {{ store.error }}
    </p>
    <p
      v-else-if="store.items.length === 0"
      class="py-16 text-center font-mono text-sm text-ink-muted"
    >
      Ничего не найдено. Попробуйте изменить фильтры.
    </p>
    <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
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
