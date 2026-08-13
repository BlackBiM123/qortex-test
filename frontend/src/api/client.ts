import axios from 'axios'
import type { ApiErrorPayload } from '@/types'

export const apiClient = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

/** Нормализованная ошибка API — то, что видят вызывающие стор-методы. */
export class ApiError extends Error {
  errors: Record<string, string | string[]>

  constructor(payload: ApiErrorPayload) {
    super(payload.detail)
    this.errors = payload.errors ?? {}
  }
}

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.detail) {
      return Promise.reject(new ApiError(error.response.data as ApiErrorPayload))
    }
    return Promise.reject(error)
  },
)
