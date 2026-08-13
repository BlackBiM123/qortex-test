<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import AppToast from '@/components/AppToast.vue'
</script>

<template>
  <header class="border-b-2 border-ink bg-surface">
    <div class="mx-auto flex max-w-5xl flex-wrap items-baseline gap-4 px-6 py-5">
      <RouterLink
        to="/"
        class="font-display text-2xl font-bold uppercase tracking-tight text-ink no-underline hover:no-underline"
      >
        Каталог<span class="text-accent">.</span>Альбомов
      </RouterLink>
      <nav class="ml-auto flex gap-6 font-mono text-xs uppercase tracking-widest">
        <RouterLink
          to="/"
          class="text-ink-muted no-underline hover:text-accent hover:no-underline [&.router-link-exact-active]:text-accent"
        >
          Альбомы
        </RouterLink>
        <RouterLink
          to="/artists"
          class="text-ink-muted no-underline hover:text-accent hover:no-underline [&.router-link-exact-active]:text-accent"
        >
          Исполнители
        </RouterLink>
        <RouterLink
          to="/songs"
          class="text-ink-muted no-underline hover:text-accent hover:no-underline [&.router-link-exact-active]:text-accent"
        >
          Песни
        </RouterLink>
      </nav>
    </div>
  </header>

  <main class="mx-auto w-full max-w-5xl flex-1 px-6 py-10">
    <RouterView />
  </main>

  <footer class="border-t border-line px-6 py-6 font-mono text-xs text-ink-faint">
    <div class="mx-auto max-w-5xl">Каталог музыкальных альбомов — Vue 3 · Django REST</div>
  </footer>

  <AppToast />
</template>
