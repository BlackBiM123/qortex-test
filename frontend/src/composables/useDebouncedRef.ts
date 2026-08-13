import { customRef } from 'vue'

export function useDebouncedRef<T>(value: T, delay = 350) {
  let timeout: ReturnType<typeof setTimeout> | undefined
  return customRef((track, trigger) => ({
    get() {
      track()
      return value
    },
    set(newValue: T) {
      clearTimeout(timeout)
      timeout = setTimeout(() => {
        value = newValue
        trigger()
      }, delay)
    },
  }))
}
