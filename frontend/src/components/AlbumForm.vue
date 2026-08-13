<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
import type { Artist } from '@/types'

export interface AlbumFormValues {
  title: string
  artist: number | null
  year: number | null
}

const props = defineProps<{
  artists: Artist[]
  initial?: Partial<AlbumFormValues>
  submitting?: boolean
}>()

const emit = defineEmits<{ submit: [values: { title: string; artist: number; year: number }] }>()

const currentYear = new Date().getFullYear()

const values = reactive<AlbumFormValues>({
  title: props.initial?.title ?? '',
  artist: props.initial?.artist ?? null,
  year: props.initial?.year ?? null,
})

watch(
  () => props.initial,
  (initial) => {
    values.title = initial?.title ?? ''
    values.artist = initial?.artist ?? null
    values.year = initial?.year ?? null
  },
)

const errors = computed(() => {
  const e: Partial<Record<keyof AlbumFormValues, string>> = {}
  if (!values.title.trim()) e.title = 'Укажите название альбома.'
  if (!values.artist) e.artist = 'Выберите исполнителя.'
  if (!values.year) {
    e.year = 'Укажите год выпуска.'
  } else if (values.year < 1860 || values.year > currentYear + 1) {
    e.year = `Год должен быть от 1860 до ${currentYear + 1}.`
  }
  return e
})

const isValid = computed(() => Object.keys(errors.value).length === 0)

function handleSubmit() {
  if (!isValid.value || !values.artist || !values.year) return
  emit('submit', { title: values.title.trim(), artist: values.artist, year: values.year })
}
</script>

<template>
  <form class="flex flex-col gap-5" @submit.prevent="handleSubmit">
    <div>
      <label
        for="album-title"
        class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
        >Название</label
      >
      <input
        id="album-title"
        v-model="values.title"
        type="text"
        autocomplete="off"
        class="w-full border border-line bg-surface px-3 py-2 text-ink focus-visible:border-accent"
      />
      <span v-if="errors.title" class="mt-1 block text-xs text-danger">{{ errors.title }}</span>
    </div>

    <div>
      <label
        for="album-artist"
        class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
        >Исполнитель</label
      >
      <select
        id="album-artist"
        v-model.number="values.artist"
        class="w-full border border-line bg-surface px-3 py-2 text-ink focus-visible:border-accent"
      >
        <option :value="null" disabled>Выберите исполнителя</option>
        <option v-for="artist in artists" :key="artist.id" :value="artist.id">
          {{ artist.name }}
        </option>
      </select>
      <span v-if="errors.artist" class="mt-1 block text-xs text-danger">{{ errors.artist }}</span>
    </div>

    <div>
      <label
        for="album-year"
        class="mb-1 block font-mono text-xs tracking-widest text-ink-muted uppercase"
        >Год выпуска</label
      >
      <input
        id="album-year"
        v-model.number="values.year"
        type="number"
        :max="currentYear + 1"
        min="1860"
        class="w-full border border-line bg-surface px-3 py-2 font-mono tabular-nums text-ink focus-visible:border-accent"
      />
      <span v-if="errors.year" class="mt-1 block text-xs text-danger">{{ errors.year }}</span>
    </div>

    <button
      type="submit"
      :disabled="!isValid || submitting"
      class="self-start bg-accent px-5 py-2.5 font-mono text-xs tracking-widest text-paper uppercase transition-colors hover:bg-accent-strong disabled:cursor-not-allowed disabled:opacity-40"
    >
      {{ submitting ? 'Сохранение…' : 'Сохранить' }}
    </button>
  </form>
</template>
