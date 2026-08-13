<script setup lang="ts">
defineProps<{ title: string }>()
const emit = defineEmits<{ close: [] }>()
</script>

<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 z-[900] flex items-center justify-center bg-ink/40 p-4"
      @click.self="emit('close')"
    >
      <div
        class="max-h-[90vh] w-full max-w-md overflow-y-auto border border-line bg-surface shadow-xl"
      >
        <div class="flex items-center justify-between border-b border-line px-6 py-4">
          <h2 class="font-display text-xl font-semibold uppercase tracking-tight text-ink">
            {{ title }}
          </h2>
          <button
            type="button"
            aria-label="Закрыть"
            class="font-mono text-xl leading-none text-ink-muted hover:text-ink"
            @click="emit('close')"
          >
            &times;
          </button>
        </div>
        <div class="p-6">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>
