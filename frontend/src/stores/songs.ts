import { defineStore } from 'pinia'
import { songsApi } from '@/api/songs'
import type { Song } from '@/types'

interface SongsState {
  items: Song[]
  count: number
  page: number
  search: string
  loading: boolean
  error: string | null
}

export const useSongsStore = defineStore('songs', {
  state: (): SongsState => ({
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

    async fetchSongs() {
      this.loading = true
      this.error = null
      try {
        const data = await songsApi.list({ search: this.search || undefined, page: this.page })
        this.items = data.results
        this.count = data.count
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Не удалось загрузить песни.'
      } finally {
        this.loading = false
      }
    },

    async deleteSong(id: number) {
      await songsApi.remove(id)
      await this.fetchSongs()
    },
  },
})
