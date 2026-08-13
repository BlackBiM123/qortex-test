import { reactive } from 'vue'

export interface ToastMessage {
  id: number
  text: string
  type: 'success' | 'error'
}

let nextId = 1
const toasts = reactive<ToastMessage[]>([])

function push(text: string, type: ToastMessage['type'] = 'success') {
  const id = nextId++
  toasts.push({ id, text, type })
  setTimeout(() => remove(id), 4000)
}

function remove(id: number) {
  const index = toasts.findIndex((t) => t.id === id)
  if (index !== -1) toasts.splice(index, 1)
}

export function useToast() {
  return {
    toasts,
    success: (text: string) => push(text, 'success'),
    error: (text: string) => push(text, 'error'),
    remove,
  }
}
