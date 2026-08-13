import { apiClient } from './client'
import type { AlbumDetail, AlbumListItem, AlbumTrack, Paginated } from '@/types'

export interface AlbumListParams {
  search?: string
  artist?: number
  year_min?: number
  year_max?: number
  page?: number
  page_size?: number
}

export interface AlbumWriteData {
  title: string
  artist: number
  year: number
}

export interface AddTrackData {
  song_id?: number
  song_title?: string
  position?: number
}

export const albumsApi = {
  list(params: AlbumListParams = {}) {
    return apiClient.get<Paginated<AlbumListItem>>('/albums/', { params }).then((r) => r.data)
  },
  get(id: number) {
    return apiClient.get<AlbumDetail>(`/albums/${id}/`).then((r) => r.data)
  },
  create(data: AlbumWriteData) {
    return apiClient.post<AlbumDetail>('/albums/', data).then((r) => r.data)
  },
  update(id: number, data: Partial<AlbumWriteData>) {
    return apiClient.patch<AlbumDetail>(`/albums/${id}/`, data).then((r) => r.data)
  },
  remove(id: number) {
    return apiClient.delete(`/albums/${id}/`)
  },
  addTrack(albumId: number, data: AddTrackData) {
    return apiClient.post<AlbumTrack>(`/albums/${albumId}/tracks/`, data).then((r) => r.data)
  },
  updateTrack(albumId: number, trackId: number, data: { position: number }) {
    return apiClient
      .patch<AlbumTrack>(`/albums/${albumId}/tracks/${trackId}/`, data)
      .then((r) => r.data)
  },
  removeTrack(albumId: number, trackId: number) {
    return apiClient.delete(`/albums/${albumId}/tracks/${trackId}/`)
  },
  reorderTracks(albumId: number, order: number[]) {
    return apiClient
      .post<AlbumTrack[]>(`/albums/${albumId}/tracks/reorder/`, { order })
      .then((r) => r.data)
  },
}
