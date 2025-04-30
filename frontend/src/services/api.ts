import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the JWT token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // If the error is due to an expired token and we haven't tried to refresh yet
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh the token
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }

        const response = await axios.post('http://localhost:5000/api/refresh', {}, {
          headers: {
            'Authorization': `Bearer ${refreshToken}`
          }
        });

        // Save the new access token
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);

        // Retry the original request with the new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return axios(originalRequest);
      } catch (refreshError) {
        // If refresh fails, clear tokens and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication functions
export const authService = {
  async login(username: string, password: string) {
    const response = await api.post('/login', { username, password });
    const { access_token, refresh_token } = response.data;

    // Store tokens
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    // Return all user data from response
    return response.data;
  },

  async register(username: string, password: string) {
    return await api.post('/register', { username, password });
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  isAuthenticated() {
    const token = localStorage.getItem('access_token');
    if (!token) return false;

    try {
      const decoded: any = jwtDecode(token);
      const currentTime = Date.now() / 1000;

      // Check if token is expired
      return decoded.exp > currentTime;
    } catch (error) {
      return false;
    }
  },

  async getCurrentUser() {
    return await api.get('/user');
  }
};

// Voice API functions
export const voiceService = {
  async generateVoice(text: string) {
    return await api.post('/voice/generate', { text });
  }
};

export default api;
