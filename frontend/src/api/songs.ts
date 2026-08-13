import { apiClient } from './client'
import type { Paginated, Song, SongLite } from '@/types'

export const songsApi = {
  list(params: { search?: string; page?: number } = {}) {
    return apiClient.get<Paginated<Song>>('/songs/', { params }).then((r) => r.data)
  },
  get(id: number) {
    return apiClient.get<Song>(`/songs/${id}/`).then((r) => r.data)
  },
  search(query: string) {
    return apiClient
      .get<Paginated<SongLite>>('/songs/', { params: { search: query, page_size: 10 } })
      .then((r) => r.data.results)
  },
  create(data: { title: string }) {
    return apiClient.post<Song>('/songs/', data).then((r) => r.data)
  },
  update(id: number, data: { title: string }) {
    return apiClient.patch<Song>(`/songs/${id}/`, data).then((r) => r.data)
  },
  remove(id: number) {
    return apiClient.delete(`/songs/${id}/`)
  },
}
