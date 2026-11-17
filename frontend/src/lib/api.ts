import axios, {
  AxiosInstance,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios'

// If NEXT_PUBLIC_API_BASE_URL is set and not empty, use it.
// In browser (deployed on Vercel or same origin), if empty or pointing to localhost when deployed, use relative '' so Vercel rewrites route to /api/index.py
const getBaseUrl = () => {
  if (typeof window !== 'undefined') {
    const envUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    
    // When deployed (e.g. on Vercel), if env points to localhost:8000, ignore it and use relative path ''
    if (!isLocalhost && (!envUrl || envUrl.includes('localhost') || envUrl.includes('127.0.0.1'))) {
      return '';
    }
    
    return envUrl || (isLocalhost ? 'http://localhost:8000' : '');
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
};

const API_BASE_URL = getBaseUrl();

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Handle 401 Unauthorized errors
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    // Check if the error is a 401 and the request was not to the login endpoint
    if (
      error.response?.status === 401 &&
      error.config.url !== '/auth/token'
    ) {
      if (typeof window !== 'undefined') {
        console.warn('Unauthorized access (401), redirecting to login.');
        // Clear auth-related data
        localStorage.removeItem('access_token');
        // Redirect to the login page
        window.location.href = '/login';
      }
    }
    // For all other errors, or for 401 on the login page, just let the promise reject
    // so that local error handlers (like in the login form) can catch it.
    return Promise.reject(error);
  }
);

export default api

/* =========================
   AUTH API
========================= */

export const authAPI = {
  register: (userData: any) => api.post('/auth/register', userData),
  login: (credentials: any) => api.post('/auth/token', credentials),
  getCurrentUser: () => api.get('/auth/me'),
}

/* =========================
   TASK API (FIXED)
========================= */

export const taskAPI = {
  // collection → slash
  getTasks: () => api.get('/tasks/'),
  createTask: (taskData: any) => api.post('/tasks/', taskData),

  // single resource → NO slash
  getTask: (taskId: string | number) => api.get(`/tasks/${taskId}`),
  updateTask: (taskId: string | number, taskData: any) =>
    api.patch(`/tasks/${taskId}`, taskData),
  deleteTask: (taskId: string | number) =>
    api.delete(`/tasks/${taskId}`),
}