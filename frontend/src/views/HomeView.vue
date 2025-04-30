<script setup lang="ts">
import { ref, computed } from 'vue'
import HeaderComponent from '../components/HeaderComponent.vue'
import SidebarComponent from '../components/SidebarComponent.vue'
import GraphWidget from '../components/GraphWidget.vue'

// Get sidebar collapsed state
const sidebarCollapsed = ref(false)

const updateSidebarState = (collapsed: boolean) => {
  sidebarCollapsed.value = collapsed
}

// Sample data for demonstration
const packageStats = [
  { name: 'vue', downloads: 1250000 },
  { name: 'react', downloads: 1800000 },
  { name: 'angular', downloads: 950000 },
  { name: 'svelte', downloads: 450000 }
]
</script>

<template>
  <div class="dashboard-layout">
    <SidebarComponent @sidebar-toggle="updateSidebarState" ref="sidebar" />

    <div class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <HeaderComponent />

      <div class="content-container">
        <h1 class="page-title">Dashboard</h1>

        <div class="widgets-grid">
          <div class="widget-container">
            <GraphWidget title="Monthly Downloads" />
          </div>

          <div class="widget-container">
            <div class="stats-card">
              <h3 class="card-title">Popular Packages</h3>
              <div class="stats-list">
                <div v-for="(pkg, index) in packageStats" :key="index" class="stat-item">
                  <div class="stat-info">
                    <span class="stat-name">{{ pkg.name }}</span>
                    <span class="stat-value">{{ pkg.downloads.toLocaleString() }}</span>
                  </div>
                  <div class="stat-bar-container">
                    <div
                      class="stat-bar"
                      :style="{ width: `${(pkg.downloads / 2000000) * 100}%` }"
                    ></div>
                  </div>
                </div>
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

.widgets-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 1024px) {
  .widgets-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.widget-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.stats-card {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-info {
  display: flex;
  justify-content: space-between;
}

.stat-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: #2c3e50;
}

.stat-value {
  font-size: 0.875rem;
  color: #6b7280;
}

.stat-bar-container {
  width: 100%;
  height: 8px;
  background-color: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.stat-bar {
  height: 100%;
  background-color: #41B883; /* Vue green color */
  border-radius: 4px;
}
</style>
