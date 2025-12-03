// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

// Type definitions for API responses
export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface Example {
  id: number;
  name: string;
  title: string;
  entryDate: string;
  description: string | null;
  isActive: boolean;
}

export interface CreateExampleDto {
  name: string;
  title: string;
  description?: string;
  isActive?: boolean;
}

export interface UpdateExampleDto {
  name?: string;
  title?: string;
  description?: string;
  isActive?: boolean;
}

export interface ApiError {
  message: string;
  status?: number;
}

// Generic fetch helper with error handling
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('An unknown error occurred');
  }
}

// API Methods
export const api = {
  // Health check endpoint
  health: {
    get: () => apiFetch<HealthResponse>('/api/health'),
  },

  // Examples endpoints
  examples: {
    getAll: () => apiFetch<Example[]>('/api/examples'),
    getById: (id: number) => apiFetch<Example>(`/api/examples/${id}`),
    search: (name: string) => apiFetch<Example[]>(`/api/examples/search?name=${encodeURIComponent(name)}`),
    create: (data: CreateExampleDto) => apiFetch<Example>('/api/examples', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id: number, data: UpdateExampleDto) => apiFetch<Example>(`/api/examples/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),
    delete: (id: number) => apiFetch<void>(`/api/examples/${id}`, {
      method: 'DELETE',
    }),
  },
};
