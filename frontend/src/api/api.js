import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth functions
export const registerUser = async (data) => {
  try {
    const response = await api.post('/auth/register', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Registration failed');
  }
};

export const login = async (credentials) => {
  try {
    // OAuth2PasswordRequestForm expects form data
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    // Store token and user
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

export const adminLogin = async (credentials) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    
    const response = await api.post('/auth/admin/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('admin', JSON.stringify(response.data.admin));
    }
    
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Admin login failed');
  }
};

// User functions
export const getUser = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch user');
  }
};

export const getCurrentUser = async () => {
  try {
    const response = await api.get('/users/me');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch current user');
  }
};

export const updateUser = async (userId, data) => {
  try {
    const response = await api.put(`/users/${userId}`, data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to update user');
  }
};

export const updateCurrentUser = async (data) => {
  try {
    const response = await api.put('/users/me', data);
    // Update stored user data
    if (response.data) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to update profile');
  }
};

// Formation functions
export const getFormations = async () => {
  try {
    const response = await api.get('/formations');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch formations');
  }
};

export const getFormation = async (formationId) => {
  try {
    const response = await api.get(`/formations/${formationId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch formation');
  }
};

export const createFormation = async (data) => {
  try {
    const response = await api.post('/formations', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to create formation');
  }
};

export const updateFormation = async (formationId, data) => {
  try {
    const response = await api.put(`/formations/${formationId}`, data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to update formation');
  }
};

export const deleteFormation = async (formationId) => {
  try {
    await api.delete(`/formations/${formationId}`);
    return true;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to delete formation');
  }
};

export const getCategories = async () => {
  try {
    const response = await api.get('/categories');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch categories');
  }
};

// Statistics
export const getStatistics = async () => {
  try {
    const response = await api.get('/api/statistics');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch statistics');
  }
};

// Recommendation functions
export const recommendKeyword = async (userId, topN = 5) => {
  try {
    const response = await api.post('/api/recommend/keyword', {
      user_id: userId,
      top_n: topN,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Keyword recommendation failed');
  }
};

export const recommendAI = async (userId, mode = 'enhance', topN = 5) => {
  try {
    const response = await api.post('/api/recommend/ai', {
      user_id: userId,
      mode: mode,
      top_n: topN,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'AI recommendation failed');
  }
};

// Job functions
export const getJobs = async () => {
  try {
    const response = await api.get('/jobs');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch jobs');
  }
};

export const getJob = async (jobId) => {
  try {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch job');
  }
};

export const createJob = async (data) => {
  try {
    const response = await api.post('/jobs', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to create job');
  }
};

export const updateJob = async (jobId, data) => {
  try {
    const response = await api.put(`/jobs/${jobId}`, data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to update job');
  }
};

export const deleteJob = async (jobId) => {
  try {
    await api.delete(`/jobs/${jobId}`);
    return true;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to delete job');
  }
};

// Admin functions
export const getAllUsers = async () => {
  try {
    const response = await api.get('/users');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch users');
  }
};

export const createUser = async (data) => {
  try {
    const response = await api.post('/users', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to create user');
  }
};

export const deleteUser = async (userId) => {
  try {
    await api.delete(`/users/${userId}`);
    return true;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to delete user');
  }
};

export default api;

