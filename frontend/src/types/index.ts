export interface Project {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface Signature {
  id: number
  project_id: number
  name: string
  description?: string
  input_fields: Record<string, any>[]
  output_fields: Record<string, any>[]
  created_at: string
}

export interface Dataset {
  id: number
  project_id: number
  signature_id: number
  name: string
  examples: Record<string, any>[]
  created_at: string
}

export interface Metric {
  id: number
  project_id: number
  signature_id: number
  name: string
  metric_type: string
  config?: Record<string, any>
  created_at: string
}

export interface Program {
  id: number
  project_id: number
  signature_id: number
  name: string
  description?: string
  code: string
  created_at: string
}

export interface OptimizationRun {
  id: number
  project_id: number
  signature_id: number
  program_id: number
  metric_id: number
  dataset_id: number
  status: 'pending' | 'running' | 'completed' | 'failed' | 'stopped'
  initial_prompt: string
  best_prompt?: string
  best_score?: number
  iterations: number
  results?: Record<string, any>[]
  created_at: string
  updated_at: string
}

export interface PromptVariation {
  id: number
  run_id: number
  prompt: string
  score: number
  iteration: number
  created_at: string
}

// Authentication Types
export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface AuthContextType {
  user: User | null
  token: string | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}
