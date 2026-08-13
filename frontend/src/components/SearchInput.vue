<script setup lang="ts">
const model = defineModel<string>({ default: '' })

defineProps<{ placeholder?: string }>()
</script>

<template>
  <div class="relative">
    <span
      class="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 font-mono text-ink-faint"
      aria-hidden="true"
      >⌕</span
    >
    <input
      v-model="model"
      type="search"
      class="w-full border border-line bg-surface py-2 pr-3 pl-9 text-ink placeholder:text-ink-faint focus-visible:border-accent"
      :placeholder="placeholder ?? 'Поиск…'"
    />
  </div>
</template>
