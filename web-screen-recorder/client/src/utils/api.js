import axios from 'axios';

// Create an axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// API methods
const apiService = {
  // Auth endpoints
  auth: {
    login: (credentials) => api.post('/auth/login', credentials),
    register: (userData) => api.post('/auth/register', userData),
    logout: () => {
      localStorage.removeItem('token');
      return Promise.resolve();
    },
    getCurrentUser: () => api.get('/auth/me'),
  },
  
  // Recordings endpoints
  recordings: {
    getAll: () => api.get('/recordings'),
    getById: (id) => api.get(`/recordings/${id}`),
    create: (recordingData) => {
      const formData = new FormData();
      formData.append('title', recordingData.title);
      formData.append('description', recordingData.description || '');
      formData.append('video', recordingData.blob, 'recording.webm');
      
      return api.post('/recordings', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    },
    update: (id, data) => api.put(`/recordings/${id}`, data),
    delete: (id) => api.delete(`/recordings/${id}`),
  },
  
  // User endpoints
  users: {
    updateProfile: (data) => api.put('/users/profile', data),
    updatePassword: (data) => api.put('/users/password', data),
  },
};

export default apiService;
