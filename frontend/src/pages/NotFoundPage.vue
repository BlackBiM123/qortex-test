<script setup lang="ts"></script>

<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Страница не найдена.</p>
    <RouterLink to="/" class="btn btn-primary">На главную</RouterLink>
  </div>
</template>

<style scoped>
.not-found {
  text-align: center;
  padding: var(--space-6) 0;
}

.not-found h1 {
  font-size: 3rem;
  margin: 0;
}
</style>
