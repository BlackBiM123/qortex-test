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
  <nav v-if="totalPages > 1" class="pagination" aria-label="Постраничная навигация">
    <button class="btn btn-secondary" type="button" :disabled="page <= 1" @click="go(page - 1)">
      ← Назад
    </button>
    <span class="page-info">{{ page }} из {{ totalPages }}</span>
    <button
      class="btn btn-secondary"
      type="button"
      :disabled="page >= totalPages"
      @click="go(page + 1)"
    >
      Вперёд →
    </button>
  </nav>
</template>

<style scoped>
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  margin-top: var(--space-5);
}

.page-info {
  color: var(--color-text-muted);
  font-size: 0.9375rem;
}
</style>
