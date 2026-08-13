import { apiClient } from './client'
import type { Artist, Paginated } from '@/types'

export const artistsApi = {
  list(params: { search?: string; page?: number; page_size?: number } = {}) {
    return apiClient.get<Paginated<Artist>>('/artists/', { params }).then((r) => r.data)
  },
  get(id: number) {
    return apiClient.get<Artist>(`/artists/${id}/`).then((r) => r.data)
  },
  create(data: { name: string }) {
    return apiClient.post<Artist>('/artists/', data).then((r) => r.data)
  },
  update(id: number, data: { name: string }) {
    return apiClient.patch<Artist>(`/artists/${id}/`, data).then((r) => r.data)
  },
  remove(id: number) {
    return apiClient.delete(`/artists/${id}/`)
  },
}
