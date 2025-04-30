<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  HomeIcon,
  UserIcon,
  SpeakerWaveIcon,
  Cog6ToothIcon,
  ChartBarIcon,
  DocumentTextIcon,
  ArrowLeftOnRectangleIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const collapsed = ref(false)

// Define emits
const emit = defineEmits(['sidebar-toggle'])

const toggleSidebar = () => {
  collapsed.value = !collapsed.value
  emit('sidebar-toggle', collapsed.value)
}

// Watch for collapsed state changes
watch(collapsed, (newValue) => {
  emit('sidebar-toggle', newValue)
})

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}

const navItems = [
  { name: 'Dashboard', icon: HomeIcon, route: '/' },
  { name: 'Voice Models', icon: SpeakerWaveIcon, route: '/voice-models' },
  { name: 'Analytics', icon: ChartBarIcon, route: '/analytics' },
  { name: 'Documents', icon: DocumentTextIcon, route: '/documents' },
  { name: 'Profile', icon: UserIcon, route: '/profile' },
  { name: 'Settings', icon: Cog6ToothIcon, route: '/settings' },
]
</script>

<template>
  <aside :class="['sidebar', { 'collapsed': collapsed }]">
    <!-- Top section with brand icon -->
    <div class="sidebar-header">
      <div class="brand-container" @click="toggleSidebar" role="button" tabindex="0">
        <div class="brand-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.5 2A1.5 1.5 0 0 0 14 3.5v13a1.5 1.5 0 0 0 1.5 1.5h1a1.5 1.5 0 0 0 1.5-1.5v-13A1.5 1.5 0 0 0 16.5 2h-1Z" />
            <path d="M9.5 6A1.5 1.5 0 0 0 8 7.5v9A1.5 1.5 0 0 0 9.5 18h1a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 10.5 6h-1Z" />
            <path d="M3.5 10A1.5 1.5 0 0 0 2 11.5v5A1.5 1.5 0 0 0 3.5 18h1A1.5 1.5 0 0 0 6 16.5v-5A1.5 1.5 0 0 0 4.5 10h-1Z" />
          </svg>
        </div>
        <span v-if="!collapsed" class="brand-name">AI Voice</span>
      </div>
    </div>

    <!-- Navigation items -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <li v-for="item in navItems" :key="item.name" class="nav-item">
          <router-link :to="item.route" class="nav-link" :title="collapsed ? item.name : ''">
            <component :is="item.icon" class="nav-icon" />
            <span v-if="!collapsed" class="nav-text">{{ item.name }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Bottom section with logout -->
    <div class="sidebar-footer">
      <button class="logout-button" @click="logout" :title="collapsed ? 'Logout' : ''">
        <ArrowLeftOnRectangleIcon class="nav-icon" />
        <span v-if="!collapsed" class="nav-text">Logout</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  background-color: #1a1a2e;
  color: #ffffff;
  height: 100vh;
  width: 250px;
  transition: width 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 50; /* Higher than header to ensure sidebar is above */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  padding: 0 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  height: 64px; /* Fixed height to match header */
}

.brand-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  overflow: hidden;
  cursor: pointer;
  padding: 0;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
  height: 100%;
}

.brand-container:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.brand-icon {
  width: 2rem;
  height: 2rem;
  color: #41B883; /* Vue green color */
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.5rem;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 600;
  white-space: nowrap;
}

.expand-indicator {
  display: flex;
  justify-content: center;
  padding: 0.5rem 0;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  background-color: rgba(255, 255, 255, 0.05);
  margin-top: 0.5rem;
}

.sidebar-nav {
  flex: 1;
  padding: 1.5rem 0;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  color: #e5e7eb;
  text-decoration: none;
  transition: background-color 0.2s, color 0.2s;
  border-radius: 0.25rem;
  margin: 0 0.5rem;
}

.nav-link:hover, .nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.nav-link.router-link-active {
  border-left: 3px solid #41B883;
}

.nav-icon {
  width: 1.5rem;
  height: 1.5rem;
  flex-shrink: 0;
}

.nav-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-footer {
  padding: 0.5rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-button {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  color: #e5e7eb;
  cursor: pointer;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
  margin-left: 0.5rem;
}

.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}
</style>
