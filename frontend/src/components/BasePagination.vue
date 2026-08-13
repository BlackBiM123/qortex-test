<script setup lang="ts">
const props = defineProps<{
  page: number
  totalPages: number
}>()
const emit = defineEmits<{ 'update:page': [page: number] }>()

function go(page: number) {
  if (page < 1 || page > props.totalPages || page === props.page) return
  emit('update:page', page)
}
</script>

<template>
  <nav
    v-if="totalPages > 1"
    class="mt-10 flex items-center justify-center gap-6"
    aria-label="Постраничная навигация"
  >
    <button
      type="button"
      class="border border-ink px-3 py-1.5 font-mono text-xs uppercase tracking-widest text-ink transition-colors hover:bg-ink hover:text-paper disabled:cursor-not-allowed disabled:border-line disabled:text-ink-faint disabled:hover:bg-transparent disabled:hover:text-ink-faint"
      :disabled="page <= 1"
      @click="go(page - 1)"
    >
      ← Назад
    </button>
    <span class="font-mono text-sm tabular-nums text-ink-muted">
      {{ String(page).padStart(2, '0') }} / {{ String(totalPages).padStart(2, '0') }}
    </span>
    <button
      type="button"
      class="border border-ink px-3 py-1.5 font-mono text-xs uppercase tracking-widest text-ink transition-colors hover:bg-ink hover:text-paper disabled:cursor-not-allowed disabled:border-line disabled:text-ink-faint disabled:hover:bg-transparent disabled:hover:text-ink-faint"
      :disabled="page >= totalPages"
      @click="go(page + 1)"
    >
      Вперёд →
    </button>
  </nav>
</template>
