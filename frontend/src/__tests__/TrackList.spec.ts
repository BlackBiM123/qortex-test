import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TrackList from '@/components/TrackList.vue'
import type { AlbumTrack } from '@/types'

const tracks: AlbumTrack[] = [
  { id: 1, position: 1, song: { id: 1, title: 'Breathe' } },
  { id: 2, position: 2, song: { id: 2, title: 'Time' } },
]

describe('TrackList', () => {
  it('renders every track with its position and title', () => {
    const wrapper = mount(TrackList, { props: { modelValue: tracks } })

    const rows = wrapper.findAll('.track-row')
    expect(rows).toHaveLength(2)
    expect(rows[0].text()).toContain('Breathe')
    expect(rows[1].text()).toContain('Time')
  })

  it('emits remove with the clicked track id', async () => {
    const wrapper = mount(TrackList, { props: { modelValue: tracks } })

    await wrapper.findAll('.remove-btn')[1].trigger('click')

    expect(wrapper.emitted('remove')).toEqual([[2]])
  })
})
