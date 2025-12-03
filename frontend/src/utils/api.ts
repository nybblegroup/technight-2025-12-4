// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';

// Type definitions for API responses
export interface HealthResponse {
  status: string;
  timestamp: string;
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
      throw new Error(`HTTP error! status: ${response.status}`);
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

  // Add more API methods here as needed
  // Example:
  // users: {
  //   getAll: () => apiFetch<User[]>('/api/users'),
  //   getById: (id: string) => apiFetch<User>(`/api/users/${id}`),
  //   create: (data: CreateUserDto) => apiFetch<User>('/api/users', {
  //     method: 'POST',
  //     body: JSON.stringify(data),
  //   }),
  // },
};
