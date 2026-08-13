<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useArtistsStore } from '@/stores/artists'
import { useToast } from '@/composables/useToast'
import { useDebouncedRef } from '@/composables/useDebouncedRef'
import SearchInput from '@/components/SearchInput.vue'
import BasePagination from '@/components/BasePagination.vue'
import BaseModal from '@/components/BaseModal.vue'

const store = useArtistsStore()
const toast = useToast()

const searchInput = ref('')
const debouncedSearch = useDebouncedRef('', 350)
const showCreateModal = ref(false)
const newName = ref('')
const submitting = ref(false)

watch(searchInput, (value) => {
  debouncedSearch.value = value
})

watch(debouncedSearch, (value) => {
  store.setSearch(value)
  store.fetchArtists()
})

function onPageChange(page: number) {
  store.setPage(page)
  store.fetchArtists()
}

async function handleCreate() {
  if (!newName.value.trim()) return
  submitting.value = true
  try {
    await store.createArtist(newName.value.trim())
    newName.value = ''
    showCreateModal.value = false
    toast.success('Исполнитель добавлен.')
  } catch {
    toast.error('Не удалось добавить исполнителя. Возможно, имя уже занято.')
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id: number) {
  if (!confirm('Удалить исполнителя вместе со всеми его альбомами?')) return
  try {
    await store.deleteArtist(id)
    toast.success('Исполнитель удалён.')
  } catch {
    toast.error('Не удалось удалить исполнителя.')
  }
}

onMounted(() => store.fetchArtists())
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Исполнители</h1>
      <button class="btn btn-primary" type="button" @click="showCreateModal = true">
        + Добавить исполнителя
      </button>
    </div>

    <SearchInput v-model="searchInput" placeholder="Поиск по имени…" />

    <p v-if="store.loading" class="state-message">Загрузка…</p>
    <p v-else-if="store.items.length === 0" class="state-message">Исполнители не найдены.</p>
    <ul v-else class="artist-list">
      <li v-for="artist in store.items" :key="artist.id" class="artist-row card">
        <RouterLink :to="`/artists/${artist.id}`">{{ artist.name }}</RouterLink>
        <span class="meta">{{ artist.albums_count }} альбомов</span>
        <button class="btn btn-danger" type="button" @click="handleDelete(artist.id)">
          Удалить
        </button>
      </li>
    </ul>

    <BasePagination
      :page="store.page"
      :total-pages="Math.max(1, Math.ceil(store.count / 20))"
      @update:page="onPageChange"
    />

    <BaseModal v-if="showCreateModal" title="Новый исполнитель" @close="showCreateModal = false">
      <form @submit.prevent="handleCreate">
        <div class="field">
          <label for="artist-name">Имя</label>
          <input id="artist-name" v-model="newName" type="text" autocomplete="off" />
        </div>
        <button class="btn btn-primary" type="submit" :disabled="submitting || !newName.trim()">
          {{ submitting ? 'Сохранение…' : 'Сохранить' }}
        </button>
      </form>
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

.artist-list {
  list-style: none;
  margin: var(--space-5) 0 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.artist-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-4);
}

.artist-row a {
  flex: 1;
  color: var(--color-text);
  font-weight: 500;
}

.meta {
  color: var(--color-text-muted);
  font-size: 0.875rem;
}
</style>
