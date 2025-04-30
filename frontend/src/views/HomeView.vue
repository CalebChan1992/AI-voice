<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

// Fetch current user data when component mounts
onMounted(() => {
  authStore.fetchCurrentUser()
})
</script>

<template>
  <div class="home-container">
    <header class="header">
      <h1>AI Voice Dashboard</h1>
      <div class="user-info">
        <span v-if="authStore.user">
          {{ authStore.user.username }} ({{ authStore.user.role }})
        </span>
        <button @click="authStore.logout()" class="logout-btn">Logout</button>
      </div>
    </header>

    <main class="main-content">
      <h2>Welcome to AI Voice</h2>
      <div v-if="authStore.user" class="user-details">
        <h3>User Information</h3>
        <p><strong>User ID:</strong> {{ authStore.user.id }}</p>
        <p><strong>Username:</strong> {{ authStore.user.username }}</p>
        <p><strong>Role:</strong> {{ authStore.user.role }}</p>
      </div>
      <p>This is your AI voice dashboard. You can manage your voice generation here.</p>
    </main>
  </div>
</template>

<style scoped>
.home-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1a1a2e;
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-details {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.user-details h3 {
  margin-top: 0;
  color: #0a6cff;
  margin-bottom: 1rem;
}

.logout-btn {
  background-color: #e94560;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c73e54;
}

.main-content {
  flex: 1;
  padding: 2rem;
}
</style>
