<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const { toasts, remove } = useToast()
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="`toast-${toast.type}`"
        @click="remove(toast.id)"
      >
        {{ toast.text }}
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  bottom: var(--space-5);
  right: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  z-index: 1000;
}

.toast {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  font-size: 0.9375rem;
  max-width: 320px;
}

.toast-success {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.toast-error {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

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
