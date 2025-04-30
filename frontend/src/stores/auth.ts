import { defineStore } from 'pinia';
import { authService } from '../services/api';

interface User {
  id: number;
  username: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  role: string;
  is_active?: boolean;
  organization_id?: number;
  created_at?: string;
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
          email: response.email,
          first_name: response.first_name,
          last_name: response.last_name,
          role: response.role,
          is_active: response.is_active,
          organization_id: response.organization_id,
          created_at: response.created_at,
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
        const userData = response.data;

        // Create user object from response data
        this.user = {
          id: userData.id || userData.user_id,
          username: userData.username,
          email: userData.email,
          first_name: userData.first_name,
          last_name: userData.last_name,
          role: userData.role,
          is_active: userData.is_active,
          organization_id: userData.organization_id,
          created_at: userData.created_at,
          token: localStorage.getItem('access_token') || undefined
        };
      } catch (error) {
        this.logout();
      } finally {
        this.loading = false;
      }
    },

    // Helper method to check if user has a specific role
    hasRole(role: string | string[]): boolean {
      if (!this.user) return false;

      if (Array.isArray(role)) {
        return role.includes(this.user.role);
      }

      return this.user.role === role;
    },

    // Helper method to check if user is an admin
    isAdmin(): boolean {
      return this.hasRole('admin');
    },

    // Helper method to check if user is a manager or admin
    isManagerOrAdmin(): boolean {
      return this.hasRole(['admin', 'manager']);
    }
  }
});
