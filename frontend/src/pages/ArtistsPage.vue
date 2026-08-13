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
    <div class="mb-8 flex flex-wrap items-baseline justify-between gap-3">
      <h1 class="font-display text-3xl font-bold tracking-tight text-ink">Исполнители</h1>
      <button
        type="button"
        class="border border-ink px-4 py-2 font-mono text-xs tracking-widest text-ink uppercase transition-colors hover:bg-ink hover:text-paper"
        @click="showCreateModal = true"
      >
        + Добавить исполнителя
      </button>
    </div>

    <SearchInput v-model="searchInput" placeholder="Поиск по имени…" />

    <p v-if="store.loading" class="py-16 text-center font-mono text-sm text-ink-muted">Загрузка…</p>
    <p
      v-else-if="store.items.length === 0"
      class="py-16 text-center font-mono text-sm text-ink-muted"
    >
      Исполнители не найдены.
    </p>
    <ul v-else class="mt-6 flex flex-col border border-line bg-surface">
      <li
        v-for="artist in store.items"
        :key="artist.id"
        class="flex items-center gap-4 border-b border-line px-4 py-3 last:border-b-0"
      >
        <RouterLink
          :to="`/artists/${artist.id}`"
          class="flex-1 font-medium text-ink no-underline hover:text-accent hover:no-underline"
          >{{ artist.name }}</RouterLink
        >
        <span class="font-mono text-xs tabular-nums text-ink-muted"
          >{{ artist.albums_count }} альбомов</span
        >
        <button
          type="button"
          class="font-mono text-xs text-danger hover:underline"
          @click="handleDelete(artist.id)"
        >
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
      <form class="flex flex-col gap-5" @submit.prevent="handleCreate">
        <div>
          <label
            for="artist-name"
            class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
            >Имя</label
          >
          <input
            id="artist-name"
            v-model="newName"
            type="text"
            autocomplete="off"
            class="w-full border border-line bg-surface px-3 py-2 text-ink focus-visible:border-accent"
          />
        </div>
        <button
          type="submit"
          :disabled="submitting || !newName.trim()"
          class="self-start bg-accent px-5 py-2.5 font-mono text-xs tracking-widest text-paper uppercase transition-colors hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-40"
        >
          {{ submitting ? 'Сохранение…' : 'Сохранить' }}
        </button>
      </form>
    </BaseModal>
  </div>
</template>
