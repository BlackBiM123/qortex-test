import axios from 'axios'
import type { ApiErrorPayload } from '@/types'

// В dev-режиме и при сборке в один контейнер с backend — относительный
// путь /api (через Vite-прокси или общий домен). При раздельном хостинге
// (например, фронт на Vercel, backend на Render) на этапе сборки задаётся
// VITE_API_BASE_URL с абсолютным адресом backend.
const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'

export const apiClient = axios.create({
  baseURL,
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
