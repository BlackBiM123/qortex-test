import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'albums',
      component: () => import('@/pages/AlbumsPage.vue'),
    },
    {
      path: '/albums/:id(\\d+)',
      name: 'album-detail',
      component: () => import('@/pages/AlbumDetailPage.vue'),
      props: true,
    },
    {
      path: '/artists',
      name: 'artists',
      component: () => import('@/pages/ArtistsPage.vue'),
    },
    {
      path: '/artists/:id(\\d+)',
      name: 'artist-detail',
      component: () => import('@/pages/ArtistDetailPage.vue'),
      props: true,
    },
    {
      path: '/songs',
      name: 'songs',
      component: () => import('@/pages/SongsPage.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/pages/NotFoundPage.vue'),
    },
  ],
})

export default router
