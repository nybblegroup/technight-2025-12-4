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

// Event Hub Types
export interface EventResponse {
  id: number;
  title: string;
  description: string | null;
  event_date: string;
  status: string;
  max_participants: number | null;
  created_at: string;
  updated_at: string;
  speaker_name: string | null;
  speaker_avatar: string | null;
  event_type: string | null;
  google_calendar_id: string | null;
  participant_count: number;
}

export interface CreateEventDto {
  title: string;
  description?: string;
  event_date: string;
  max_participants?: number;
  speaker_name?: string;
  speaker_avatar?: string;
  event_type?: string;
}

export interface ParticipantResponse {
  id: number;
  event_id: number;
  user_id: string;
  name: string;
  email: string;
  avatar_url: string | null;
  points: number;
  streak: number;
  rank_position: number | null;
  responses_count: number;
  quality_score: number;
  sentiment_score: number;
  joined_at: string;
  last_activity_at: string | null;
}

export interface RankingResponse {
  position: number;
  participant: ParticipantResponse;
  badges: string[];
}

export interface QuestionResponse {
  id: number;
  event_id: number;
  text: string;
  question_type: string;
  order: number;
  options: string[] | null;
  is_ai_generated: boolean;
  asked_at: string | null;
}

export interface CreateQuestionDto {
  event_id: number;
  text: string;
  question_type?: string;
  order?: number;
  options?: string[];
  is_ai_generated?: boolean;
  ai_context?: string;
}

export interface ResponseResponse {
  id: number;
  question_id: number;
  participant_id: number;
  text: string;
  rating: number | null;
  sentiment: string | null;
  sentiment_score: number | null;
  quality_score: number | null;
  points_awarded: number;
  created_at: string;
  participant_name: string | null;
}

export interface CreateResponseDto {
  question_id: number;
  participant_id: number;
  text: string;
  rating?: number;
  is_quick_option?: boolean;
}

export interface MessageResponse {
  id: number;
  event_id: number;
  participant_id: number | null;
  text: string;
  message_type: string;
  created_at: string;
  participant_name: string | null;
  participant_avatar: string | null;
}

export interface CreateMessageDto {
  event_id: number;
  participant_id?: number;
  text: string;
  message_type?: string;
}

export interface NybblerDto {
  id: string;
  name: string;
  email: string;
  avatar_url: string;
  department: string | null;
  position: string | null;
}

export interface BadgeResponse {
  id: number;
  name: string;
  display_name: string;
  description: string;
  icon: string;
  criteria_type: string;
  criteria_value: number;
  rarity: string;
}

export interface EventStatsResponse {
  event_id: number;
  total_participants: number;
  total_responses: number;
  average_quality_score: number;
  average_sentiment_score: number;
  completion_rate: number;
  top_participants: RankingResponse[];
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

  // Events endpoints
  events: {
    getAll: (status?: string) => apiFetch<EventResponse[]>(`/api/events${status ? `?status=${status}` : ''}`),
    getById: (id: number) => apiFetch<EventResponse>(`/api/events/${id}`),
    create: (data: CreateEventDto) => apiFetch<EventResponse>('/api/events', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    update: (id: number, data: Partial<CreateEventDto>) => apiFetch<EventResponse>(`/api/events/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),
    delete: (id: number) => apiFetch<void>(`/api/events/${id}`, {
      method: 'DELETE',
    }),
    getStats: (id: number) => apiFetch<EventStatsResponse>(`/api/events/${id}/stats`),
    getRankings: (id: number, limit?: number) => apiFetch<RankingResponse[]>(`/api/events/${id}/rankings${limit ? `?limit=${limit}` : ''}`),
    start: (id: number) => apiFetch<{message: string; status: string}>(`/api/events/${id}/start`, {
      method: 'POST',
    }),
    complete: (id: number) => apiFetch<{message: string; status: string}>(`/api/events/${id}/complete`, {
      method: 'POST',
    }),
  },

  // Participants endpoints
  participants: {
    join: (data: {event_id: number; user_id: string; name: string; email: string; avatar_url?: string}) => 
      apiFetch<ParticipantResponse>('/api/participants', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    getById: (id: number) => apiFetch<ParticipantResponse>(`/api/participants/${id}`),
    getStats: (id: number) => apiFetch<any>(`/api/participants/${id}/stats`),
    getBadges: (id: number) => apiFetch<any[]>(`/api/participants/${id}/badges`),
    reset: (id: number) => apiFetch<{message: string; participant_id: number; points: number}>(`/api/participants/${id}/reset`, {
      method: 'POST',
    }),
  },

  // Questions endpoints
  questions: {
    getAll: (event_id?: number) => apiFetch<QuestionResponse[]>(`/api/questions${event_id ? `?event_id=${event_id}` : ''}`),
    getById: (id: number) => apiFetch<QuestionResponse>(`/api/questions/${id}`),
    create: (data: CreateQuestionDto) => apiFetch<QuestionResponse>('/api/questions', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    generate: (data: {event_id: number; context: string; previous_questions?: string[]}) => 
      apiFetch<any>('/api/questions/generate', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    delete: (id: number) => apiFetch<void>(`/api/questions/${id}`, {
      method: 'DELETE',
    }),
  },

  // Responses endpoints
  responses: {
    getAll: (question_id?: number, participant_id?: number) => {
      const params = new URLSearchParams();
      if (question_id) params.append('question_id', question_id.toString());
      if (participant_id) params.append('participant_id', participant_id.toString());
      return apiFetch<ResponseResponse[]>(`/api/responses${params.toString() ? `?${params.toString()}` : ''}`);
    },
    getById: (id: number) => apiFetch<ResponseResponse>(`/api/responses/${id}`),
    create: (data: CreateResponseDto) => apiFetch<ResponseResponse>('/api/responses', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    getTopQuality: (event_id: number, limit?: number) => 
      apiFetch<ResponseResponse[]>(`/api/responses/top/quality?event_id=${event_id}${limit ? `&limit=${limit}` : ''}`),
  },

  // Messages endpoints
  messages: {
    getAll: (event_id: number, limit?: number) => 
      apiFetch<MessageResponse[]>(`/api/messages?event_id=${event_id}${limit ? `&limit=${limit}` : ''}`),
    create: (data: CreateMessageDto) => apiFetch<MessageResponse>('/api/messages', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
    delete: (id: number) => apiFetch<void>(`/api/messages/${id}`, {
      method: 'DELETE',
    }),
  },

  // Nybblers endpoints (People Force mock)
  nybblers: {
    getAll: () => apiFetch<NybblerDto[]>('/api/nybblers'),
    search: (query: string) => apiFetch<NybblerDto[]>(`/api/nybblers/search?query=${encodeURIComponent(query)}`),
    getById: (id: string) => apiFetch<NybblerDto>(`/api/nybblers/${id}`),
  },
};
