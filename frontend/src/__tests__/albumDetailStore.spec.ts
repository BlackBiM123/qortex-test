import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAlbumDetailStore } from '@/stores/albumDetail'
import { albumsApi } from '@/api/albums'
import type { AlbumTrack } from '@/types'

vi.mock('@/api/albums', () => ({
  albumsApi: {
    get: vi.fn(),
    reorderTracks: vi.fn(),
    removeTrack: vi.fn(),
    addTrack: vi.fn(),
  },
}))

const mockedReorder = vi.mocked(albumsApi.reorderTracks)

function track(id: number, position: number): AlbumTrack {
  return { id, position, song: { id, title: `Song ${id}` } }
}

describe('useAlbumDetailStore — reorderTracks (drag&drop)', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('applies the new order optimistically before the server responds', async () => {
    const store = useAlbumDetailStore()
    store.album = {
      id: 1,
      title: 'Album',
      artist: 1,
      artist_name: 'Artist',
      year: 2000,
      tracks: [track(1, 1), track(2, 2), track(3, 3)],
    }

    let resolveRequest!: (value: AlbumTrack[]) => void
    mockedReorder.mockReturnValue(
      new Promise((resolve) => {
        resolveRequest = resolve
      }),
    )

    const newOrder = [track(3, 3), track(1, 1), track(2, 2)]
    const pending = store.reorderTracks(newOrder)

    // До ответа сервера локальный порядок уже обновлён (оптимистично).
    expect(store.album.tracks.map((t) => t.id)).toEqual([3, 1, 2])

    resolveRequest([track(3, 1), track(1, 2), track(2, 3)])
    await pending

    expect(store.album.tracks.map((t) => t.position)).toEqual([1, 2, 3])
  })

  it('rolls back to the previous order when the server rejects the change', async () => {
    const store = useAlbumDetailStore()
    const original = [track(1, 1), track(2, 2), track(3, 3)]
    store.album = {
      id: 1,
      title: 'Album',
      artist: 1,
      artist_name: 'Artist',
      year: 2000,
      tracks: original,
    }

    mockedReorder.mockRejectedValue(new Error('Список должен содержать ровно все треки альбома.'))

    const newOrder = [track(3, 3), track(1, 1), track(2, 2)]
    await expect(store.reorderTracks(newOrder)).rejects.toThrow()

    expect(store.album.tracks).toStrictEqual(original)
    expect(store.error).toContain('Список должен содержать')
  })
})
