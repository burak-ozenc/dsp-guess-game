import type {
  Difficulty,
  StartSessionResponse,
  HintResponse,
  GuessResponse,
  RevealResponse,
} from '../types/game'

// @ts-ignore
const BASE_URL = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000') + '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const error = await res.json().catch(() => ({}))
    throw new Error((error as any).detail ?? `Request failed: ${res.status}`)
  }
  return res.json()
}

export const api = {
  startSession: (difficulty: Difficulty) =>
    request<StartSessionResponse>('/sessions', {
      method: 'POST',
      body: JSON.stringify({ difficulty }),
    }),

  useHint: (sessionId: string) =>
    request<HintResponse>(`/sessions/${sessionId}/hint`, { method: 'POST' }),

  submitGuess: (sessionId: string, answer: string) =>
    request<GuessResponse>(`/sessions/${sessionId}/guess`, {
      method: 'POST',
      body: JSON.stringify({ answer }),
    }),

  reveal: (sessionId: string) =>
    request<RevealResponse>(`/sessions/${sessionId}/reveal`),

  getCategories: () => request<string[]>('/sessions/categories'),
}
