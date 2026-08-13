import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AlbumForm from '@/components/AlbumForm.vue'

const artists = [
  { id: 1, name: 'Pink Floyd', albums_count: 2 },
  { id: 2, name: 'Queen', albums_count: 1 },
]

describe('AlbumForm', () => {
  it('does not emit submit when required fields are empty', async () => {
    const wrapper = mount(AlbumForm, { props: { artists } })

    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toBeUndefined()
    expect(wrapper.text()).toContain('Укажите название альбома.')
    expect(wrapper.text()).toContain('Выберите исполнителя.')
    expect(wrapper.text()).toContain('Укажите год выпуска.')
  })

  it('rejects a year below the allowed minimum', async () => {
    const wrapper = mount(AlbumForm, { props: { artists } })

    await wrapper.find('#album-title').setValue('The Wall')
    await wrapper.find('#album-artist').setValue('1')
    await wrapper.find('#album-year').setValue('1500')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toBeUndefined()
    expect(wrapper.text()).toMatch(/Год должен быть от 1860/)
  })

  it('rejects a year further than one year in the future', async () => {
    const wrapper = mount(AlbumForm, { props: { artists } })
    const farFuture = new Date().getFullYear() + 5

    await wrapper.find('#album-title').setValue('Unreleased')
    await wrapper.find('#album-artist').setValue('1')
    await wrapper.find('#album-year').setValue(String(farFuture))
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toBeUndefined()
  })

  it('emits submit with trimmed values when the form is valid', async () => {
    const wrapper = mount(AlbumForm, { props: { artists } })

    await wrapper.find('#album-title').setValue('  The Wall  ')
    await wrapper.find('#album-artist').setValue('1')
    await wrapper.find('#album-year').setValue('1979')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.emitted('submit')).toHaveLength(1)
    expect(wrapper.emitted('submit')![0]).toEqual([{ title: 'The Wall', artist: 1, year: 1979 }])
  })

  it('pre-fills values when editing an existing album', () => {
    const wrapper = mount(AlbumForm, {
      props: { artists, initial: { title: 'Animals', artist: 1, year: 1977 } },
    })

    expect((wrapper.find('#album-title').element as HTMLInputElement).value).toBe('Animals')
    expect((wrapper.find('#album-year').element as HTMLInputElement).value).toBe('1977')
  })
})
