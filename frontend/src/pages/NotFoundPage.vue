<script setup lang="ts"></script>

<template>
  <div class="flex flex-col items-center gap-4 py-24 text-center">
    <p class="font-mono text-sm tracking-widest text-ink-faint uppercase">
      Каталожная карточка не найдена
    </p>
    <h1 class="font-display text-7xl font-bold text-ink">404</h1>
    <p class="text-ink-muted">Страница не найдена.</p>
    <RouterLink
      to="/"
      class="mt-2 border border-ink px-5 py-2.5 font-mono text-xs tracking-widest text-ink uppercase no-underline transition-colors hover:bg-ink hover:text-paper hover:no-underline"
    >
      На главную
    </RouterLink>
  </div>
</template>
