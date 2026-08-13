export interface Artist {
  id: number
  name: string
  albums_count: number
}

export interface AlbumListItem {
  id: number
  title: string
  artist: number
  artist_name: string
  year: number
  tracks_count: number
}

export interface SongLite {
  id: number
  title: string
}

export interface AlbumTrack {
  id: number
  song: SongLite
  position: number
}

export interface AlbumDetail {
  id: number
  title: string
  artist: number
  artist_name: string
  year: number
  tracks: AlbumTrack[]
}

export interface SongAlbumEntry {
  id: number
  album_id: number
  album_title: string
  artist_name: string
  year: number
  position: number
}

export interface Song {
  id: number
  title: string
  albums: SongAlbumEntry[]
}

export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ApiErrorPayload {
  detail: string
  errors: Record<string, string | string[]>
}

export interface AlbumFilters {
  search: string
  artist: number | null
  year_min: number | null
  year_max: number | null
  page: number
}
