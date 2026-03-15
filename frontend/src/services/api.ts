import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include JWT token in all requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Projects
export const projectsAPI = {
  list: () => apiClient.get('/api/projects/'),
  create: (data: any) => apiClient.post('/api/projects/', data),
  get: (id: number) => apiClient.get(`/api/projects/${id}`),
  update: (id: number, data: any) => apiClient.put(`/api/projects/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/projects/${id}`),
}

// Signatures
export const signaturesAPI = {
  list: (projectId?: number) => 
    apiClient.get('/api/signatures/', { params: { project_id: projectId } }),
  create: (data: any) => apiClient.post('/api/signatures/', data),
  get: (id: number) => apiClient.get(`/api/signatures/${id}`),
  update: (id: number, data: any) => apiClient.put(`/api/signatures/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/signatures/${id}`),
}

// Datasets
export const datasetsAPI = {
  list: (projectId?: number) =>
    apiClient.get('/api/datasets/', { params: { project_id: projectId } }),
  create: (data: any) => apiClient.post('/api/datasets/', data),
  get: (id: number) => apiClient.get(`/api/datasets/${id}`),
  update: (id: number, data: any) => apiClient.put(`/api/datasets/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/datasets/${id}`),
}

// Metrics
export const metricsAPI = {
  list: (projectId?: number) =>
    apiClient.get('/api/metrics/', { params: { project_id: projectId } }),
  create: (data: any) => apiClient.post('/api/metrics/', data),
  get: (id: number) => apiClient.get(`/api/metrics/${id}`),
  update: (id: number, data: any) => apiClient.put(`/api/metrics/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/metrics/${id}`),
}

// Programs
export const programsAPI = {
  list: (projectId?: number) =>
    apiClient.get('/api/programs/', { params: { project_id: projectId } }),
  create: (data: any) => apiClient.post('/api/programs/', data),
  get: (id: number) => apiClient.get(`/api/programs/${id}`),
  update: (id: number, data: any) => apiClient.put(`/api/programs/${id}`, data),
  delete: (id: number) => apiClient.delete(`/api/programs/${id}`),
}

// Optimization
export const optimizationAPI = {
  listRuns: (projectId?: number) =>
    apiClient.get('/api/optimization/runs', { params: { project_id: projectId } }),
  startRun: (data: any) => apiClient.post('/api/optimization/run', data),
  getRun: (id: number) => apiClient.get(`/api/optimization/${id}`),
  getVariations: (id: number) => apiClient.get(`/api/optimization/${id}/variations`),
  stopRun: (id: number) => apiClient.post(`/api/optimization/${id}/stop`),
}

// Main API client (default and named exports for flexibility)
export { apiClient as api }
export default apiClient
