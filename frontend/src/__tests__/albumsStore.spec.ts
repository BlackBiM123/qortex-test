import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAlbumsStore } from '@/stores/albums'
import { albumsApi } from '@/api/albums'

vi.mock('@/api/albums', () => ({
  albumsApi: {
    list: vi.fn(),
    remove: vi.fn(),
  },
}))

const mockedList = vi.mocked(albumsApi.list)
const mockedRemove = vi.mocked(albumsApi.remove)

function makeAlbum(id: number, overrides: Partial<Record<string, unknown>> = {}) {
  return {
    id,
    title: `Album ${id}`,
    artist: 1,
    artist_name: 'Artist',
    year: 2000,
    tracks_count: 3,
    ...overrides,
  }
}

describe('useAlbumsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetches albums and stores results with pagination info', async () => {
    mockedList.mockResolvedValue({
      count: 2,
      next: null,
      previous: null,
      results: [makeAlbum(1), makeAlbum(2)],
    })

    const store = useAlbumsStore()
    await store.fetchAlbums()

    expect(store.items).toHaveLength(2)
    expect(store.count).toBe(2)
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('passes current filters and page to the API call', async () => {
    mockedList.mockResolvedValue({ count: 0, next: null, previous: null, results: [] })

    const store = useAlbumsStore()
    store.setFilters({ search: 'floyd', artist: 3, yearMin: 1970, yearMax: 1980 })
    store.setPage(2)
    await store.fetchAlbums()

    expect(mockedList).toHaveBeenCalledWith({
      search: 'floyd',
      artist: 3,
      year_min: 1970,
      year_max: 1980,
      page: 2,
    })
  })

  it('resets to page 1 whenever filters change', async () => {
    mockedList.mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    const store = useAlbumsStore()
    store.setPage(3)

    store.setFilters({ search: 'new query' })

    expect(store.page).toBe(1)
  })

  it('computes totalPages from count and pageSize', () => {
    const store = useAlbumsStore()
    store.count = 45
    store.pageSize = 20
    expect(store.totalPages).toBe(3)
  })

  it('records an error message when the API call fails', async () => {
    mockedList.mockRejectedValue(new Error('Network down'))
    const store = useAlbumsStore()

    await store.fetchAlbums()

    expect(store.error).toBe('Network down')
    expect(store.items).toEqual([])
  })

  it('deletes an album and refreshes the list', async () => {
    mockedRemove.mockResolvedValue({} as never)
    mockedList.mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    const store = useAlbumsStore()

    await store.deleteAlbum(7)

    expect(mockedRemove).toHaveBeenCalledWith(7)
    expect(mockedList).toHaveBeenCalled()
  })
})
