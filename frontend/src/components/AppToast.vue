<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const { toasts, remove } = useToast()
</script>

<template>
  <div class="fixed right-6 bottom-6 z-[1000] flex flex-col gap-2">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="flex max-w-xs cursor-pointer items-stretch border bg-surface shadow-lg"
        :class="toast.type === 'success' ? 'border-success/40' : 'border-danger/40'"
        @click="remove(toast.id)"
      >
        <span
          class="w-1.5 shrink-0"
          :class="toast.type === 'success' ? 'bg-success' : 'bg-danger'"
        />
        <p class="px-4 py-3 text-sm text-ink">{{ toast.text }}</p>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
