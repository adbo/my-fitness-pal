import type {
  ProgressionChainList,
  ProgressionChain,
  ProgressionStatus,
  RecordWorkoutResponse,
  Exercise,
} from '../types';

const API_BASE = '/api';

async function fetchApi<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || 'API error');
  }

  return response.json();
}

export const api = {
  // Progressions
  getProgressions: () =>
    fetchApi<ProgressionChainList[]>('/progressions'),

  getProgression: (chainId: string) =>
    fetchApi<ProgressionChain>(`/progressions/${chainId}`),

  getExercise: (exerciseId: string) =>
    fetchApi<Exercise>(`/exercises/${exerciseId}`),

  // User progressions
  getUserProgressions: (username: string) =>
    fetchApi<ProgressionStatus[]>(`/users/${username}/progressions`),

  getUserProgression: (username: string, chainId: string) =>
    fetchApi<ProgressionStatus>(`/users/${username}/progressions/${chainId}`),

  startProgression: (username: string, chainId: string) =>
    fetchApi<{ message: string }>(`/users/${username}/progressions/${chainId}/start`, {
      method: 'POST',
    }),

  recordWorkout: (username: string, chainId: string, sets: number, reps: number) =>
    fetchApi<RecordWorkoutResponse>(`/users/${username}/progressions/${chainId}/record`, {
      method: 'POST',
      body: JSON.stringify({ sets, reps }),
    }),

  advanceProgression: (username: string, chainId: string) =>
    fetchApi<{ message: string; success: boolean }>(`/users/${username}/progressions/${chainId}/advance`, {
      method: 'POST',
    }),

  regressProgression: (username: string, chainId: string) =>
    fetchApi<{ message: string; success: boolean }>(`/users/${username}/progressions/${chainId}/regress`, {
      method: 'POST',
    }),

  // Users
  createUser: (username: string) =>
    fetchApi<{ id: number; username: string }>('/users', {
      method: 'POST',
      body: JSON.stringify({ username }),
    }),
};
