import { defineStore } from 'pinia'
import { albumsApi, type AddTrackData } from '@/api/albums'
import type { AlbumDetail, AlbumTrack } from '@/types'

interface AlbumDetailState {
  album: AlbumDetail | null
  loading: boolean
  error: string | null
}

export const useAlbumDetailStore = defineStore('albumDetail', {
  state: (): AlbumDetailState => ({
    album: null,
    loading: false,
    error: null,
  }),

  actions: {
    async fetchAlbum(id: number) {
      this.loading = true
      this.error = null
      try {
        this.album = await albumsApi.get(id)
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Не удалось загрузить альбом.'
      } finally {
        this.loading = false
      }
    },

    async addTrack(data: AddTrackData) {
      if (!this.album) return
      const track = await albumsApi.addTrack(this.album.id, data)
      this.album.tracks.push(track)
      this.album.tracks.sort((a, b) => a.position - b.position)
    },

    async removeTrack(trackId: number) {
      if (!this.album) return
      await albumsApi.removeTrack(this.album.id, trackId)
      this.album.tracks = this.album.tracks.filter((t) => t.id !== trackId)
    },

    /**
     * Оптимистично применяет новый порядок треков локально, затем шлёт его на
     * сервер. При ошибке откатывает к переданному предыдущему состоянию —
     * так UI никогда не расходится с сервером даже при сбое сети.
     */
    async reorderTracks(newOrder: AlbumTrack[]) {
      if (!this.album) return
      const previous = this.album.tracks
      this.album.tracks = newOrder

      try {
        const updated = await albumsApi.reorderTracks(
          this.album.id,
          newOrder.map((t) => t.id),
        )
        this.album.tracks = updated
      } catch (e) {
        this.album.tracks = previous
        this.error = e instanceof Error ? e.message : 'Не удалось изменить порядок треков.'
        throw e
      }
    },
  },
})
