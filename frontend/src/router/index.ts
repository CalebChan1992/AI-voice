import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '../services/api'
import { useAuthStore } from '../stores/auth'

// Import views
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('../views/DashboardLayout.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guest: true }
    },
    // User management routes (admin only)
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/AdminDashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('../views/admin/UserManagement.vue'),
          meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
          path: 'users/create',
          name: 'admin-users-create',
          component: () => import('../views/admin/UserForm.vue'),
          meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
          path: 'users/:id',
          name: 'admin-users-edit',
          component: () => import('../views/admin/UserForm.vue'),
          meta: { requiresAuth: true, requiresAdmin: true },
          props: true
        },
        {
          path: 'organizations',
          name: 'admin-organizations',
          component: () => import('../views/admin/OrganizationManagement.vue'),
          meta: { requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    // User profile
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    // Voice models
    {
      path: '/voice-models',
      name: 'voice-models',
      component: () => import('../views/VoiceModelsView.vue'),
      meta: { requiresAuth: true }
    },
    // Analytics
    {
      path: '/analytics',
      name: 'analytics',
      component: () => import('../views/AnalyticsView.vue'),
      meta: { requiresAuth: true, requiresManager: true }
    },
    // Settings
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsView.vue'),
      meta: { requiresAuth: true }
    },
    // Redirect any unknown routes to login
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  const isAuthenticated = authService.isAuthenticated()

  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'login' })
      return
    }

    // If we need to check roles, initialize the auth store
    if (to.matched.some(record => record.meta.requiresAdmin || record.meta.requiresManager)) {
      const authStore = useAuthStore()

      // Check if route requires admin role
      if (to.matched.some(record => record.meta.requiresAdmin) && !authStore.isAdmin()) {
        next({ name: 'dashboard' }) // Redirect to dashboard if not admin
        return
      }

      // Check if route requires manager role
      if (to.matched.some(record => record.meta.requiresManager) && !authStore.isManagerOrAdmin()) {
        next({ name: 'dashboard' }) // Redirect to dashboard if not manager or admin
        return
      }
    }

    next() // User is authenticated and has required role
  } else if (to.matched.some(record => record.meta.guest) && isAuthenticated) {
    // If user is already logged in, redirect to dashboard
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
