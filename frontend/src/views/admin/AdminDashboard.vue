<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import HeaderComponent from '../../components/HeaderComponent.vue'
import SidebarComponent from '../../components/SidebarComponent.vue'

// Get sidebar collapsed state
const sidebarCollapsed = ref(false)

const updateSidebarState = (collapsed: boolean) => {
  sidebarCollapsed.value = collapsed
}
</script>

<template>
  <div class="dashboard-layout">
    <SidebarComponent @sidebar-toggle="updateSidebarState" />

    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <HeaderComponent />

      <div class="content-container">
        <h1 class="page-title">Admin Dashboard</h1>
        
        <div class="admin-content">
          <!-- Router view for nested admin routes -->
          <router-view />
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

.admin-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}
</style>
