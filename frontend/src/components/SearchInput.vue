<script setup lang="ts">
const model = defineModel<string>({ default: '' })

defineProps<{ placeholder?: string }>()
</script>

<template>
  <input
    v-model="model"
    type="search"
    class="search-input"
    :placeholder="placeholder ?? 'Поиск…'"
  />
</template>

<style scoped>
.search-input {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  color: var(--color-text);
}

.search-input:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: -1px;
}
</style>
