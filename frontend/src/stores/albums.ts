import { defineStore } from 'pinia'
import { albumsApi } from '@/api/albums'
import type { AlbumListItem } from '@/types'

interface AlbumsState {
  items: AlbumListItem[]
  count: number
  page: number
  pageSize: number
  loading: boolean
  error: string | null
  filters: {
    search: string
    artist: number | null
    yearMin: number | null
    yearMax: number | null
  }
}

const DEFAULT_PAGE_SIZE = 20

export const useAlbumsStore = defineStore('albums', {
  state: (): AlbumsState => ({
    items: [],
    count: 0,
    page: 1,
    pageSize: DEFAULT_PAGE_SIZE,
    loading: false,
    error: null,
    filters: { search: '', artist: null, yearMin: null, yearMax: null },
  }),

  getters: {
    totalPages(state): number {
      return Math.max(1, Math.ceil(state.count / state.pageSize))
    },
  },

  actions: {
    setFilters(filters: Partial<AlbumsState['filters']>) {
      this.filters = { ...this.filters, ...filters }
      this.page = 1
    },

    setPage(page: number) {
      this.page = page
    },

    async fetchAlbums() {
      this.loading = true
      this.error = null
      try {
        const data = await albumsApi.list({
          search: this.filters.search || undefined,
          artist: this.filters.artist ?? undefined,
          year_min: this.filters.yearMin ?? undefined,
          year_max: this.filters.yearMax ?? undefined,
          page: this.page,
        })
        this.items = data.results
        this.count = data.count
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Не удалось загрузить альбомы.'
      } finally {
        this.loading = false
      }
    },

    async deleteAlbum(id: number) {
      await albumsApi.remove(id)
      await this.fetchAlbums()
    },
  },
})
