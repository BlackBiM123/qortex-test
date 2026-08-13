import { defineStore } from 'pinia'
import { artistsApi } from '@/api/artists'
import type { Artist } from '@/types'

interface ArtistsState {
  items: Artist[]
  count: number
  page: number
  search: string
  loading: boolean
  error: string | null
}

export const useArtistsStore = defineStore('artists', {
  state: (): ArtistsState => ({
    items: [],
    count: 0,
    page: 1,
    search: '',
    loading: false,
    error: null,
  }),

  actions: {
    setSearch(search: string) {
      this.search = search
      this.page = 1
    },

    setPage(page: number) {
      this.page = page
    },

    async fetchArtists() {
      this.loading = true
      this.error = null
      try {
        const data = await artistsApi.list({ search: this.search || undefined, page: this.page })
        this.items = data.results
        this.count = data.count
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Не удалось загрузить исполнителей.'
      } finally {
        this.loading = false
      }
    },

    async createArtist(name: string) {
      await artistsApi.create({ name })
      await this.fetchArtists()
    },

    async deleteArtist(id: number) {
      await artistsApi.remove(id)
      await this.fetchArtists()
    },
  },
})
