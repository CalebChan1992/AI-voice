<script setup lang="ts">
import { ref, computed } from 'vue'
import HeaderComponent from '../components/HeaderComponent.vue'
import SidebarComponent from '../components/SidebarComponent.vue'
import { useAuthStore } from '../stores/auth'

// Get sidebar collapsed state
const sidebarCollapsed = ref(false)
const authStore = useAuthStore()

const updateSidebarState = (collapsed: boolean) => {
  sidebarCollapsed.value = collapsed
}

// Get user data
const user = computed(() => authStore.user)
</script>

<template>
  <div class="dashboard-layout">
    <SidebarComponent @sidebar-toggle="updateSidebarState" />

    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <HeaderComponent />

      <div class="content-container">
        <h1 class="page-title">User Profile</h1>

        <div class="profile-container" v-if="user">
          <div class="profile-card">
            <div class="profile-header">
              <div class="profile-avatar">
                {{ user.username.charAt(0).toUpperCase() }}
              </div>
              <div class="profile-info">
                <h2 class="profile-name">
                  {{ user.first_name }} {{ user.last_name }}
                  <span v-if="!user.first_name && !user.last_name">{{ user.username }}</span>
                </h2>
                <div class="profile-role">{{ user.role }}</div>
              </div>
            </div>
            
            <div class="profile-details">
              <div class="detail-item">
                <div class="detail-label">Username</div>
                <div class="detail-value">{{ user.username }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Email</div>
                <div class="detail-value">{{ user.email || 'Not set' }}</div>
              </div>
              
              <div class="detail-item">
                <div class="detail-label">Role</div>
                <div class="detail-value">{{ user.role }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f9fafb;
}

.main-content {
  flex: 1;
  margin-left: 250px; /* Match sidebar width */
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.main-content.sidebar-collapsed {
  margin-left: 70px; /* Match collapsed sidebar width */
}

.content-container {
  padding: 2rem;
}

.page-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.profile-container {
  max-width: 800px;
}

.profile-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 2rem;
  background-color: #f3f4f6;
}

.profile-avatar {
  width: 5rem;
  height: 5rem;
  border-radius: 9999px;
  background-color: #41B883;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 600;
  margin-right: 1.5rem;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.profile-role {
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: capitalize;
}

.profile-details {
  padding: 2rem;
}

.detail-item {
  display: flex;
  margin-bottom: 1.5rem;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-label {
  width: 8rem;
  font-weight: 500;
  color: #6b7280;
}

.detail-value {
  flex: 1;
  color: #1f2937;
}
</style>
