import { defineStore } from 'pinia';
import { authService } from '../services/api';

interface User {
  id: number;
  username: string;
  role: string;
  token?: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: authService.isAuthenticated(),
    loading: false,
    error: null,
  }),

  actions: {
    async login(username: string, password: string) {
      this.loading = true;
      this.error = null;

      try {
        const response = await authService.login(username, password);

        // Create user object from response data
        this.user = {
          id: response.user_id,
          username: response.username,
          role: response.role,
          token: response.access_token
        };

        this.isAuthenticated = true;
        return true;
      } catch (error: any) {
        this.error = error.response?.data?.msg || 'Login failed';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async register(username: string, password: string) {
      this.loading = true;
      this.error = null;

      try {
        await authService.register(username, password);
        return true;
      } catch (error: any) {
        this.error = error.response?.data?.msg || 'Registration failed';
        return false;
      } finally {
        this.loading = false;
      }
    },

    logout() {
      authService.logout();
      this.user = null;
      this.isAuthenticated = false;
    },

    async fetchCurrentUser() {
      if (!this.isAuthenticated) return;

      this.loading = true;

      try {
        const response = await authService.getCurrentUser();

        // Create user object from response data
        this.user = {
          id: response.data.user_id,
          username: response.data.username,
          role: response.data.role,
          token: localStorage.getItem('access_token') || undefined
        };
      } catch (error) {
        this.logout();
      } finally {
        this.loading = false;
      }
    }
  }
});
