<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import AppToast from '@/components/AppToast.vue'
</script>

<template>
  <header class="app-header">
    <div class="container header-inner">
      <RouterLink to="/" class="logo">🎵 Каталог альбомов</RouterLink>
      <nav class="nav-links">
        <RouterLink to="/">Альбомы</RouterLink>
        <RouterLink to="/artists">Исполнители</RouterLink>
        <RouterLink to="/songs">Песни</RouterLink>
      </nav>
    </div>
  </header>

  <main class="container app-main">
    <RouterView />
  </main>

  <AppToast />
</template>

<style scoped>
.app-header {
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--space-4);
  padding-bottom: var(--space-4);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.logo {
  font-weight: 700;
  font-size: 1.125rem;
  color: var(--color-text);
}

.logo:hover {
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: var(--space-5);
}

.nav-links a {
  color: var(--color-text-muted);
  font-weight: 500;
}

.nav-links a:hover {
  color: var(--color-primary);
  text-decoration: none;
}

.nav-links a.router-link-exact-active {
  color: var(--color-primary);
}

.app-main {
  flex: 1;
  padding-top: var(--space-6);
  padding-bottom: var(--space-6);
}
</style>
