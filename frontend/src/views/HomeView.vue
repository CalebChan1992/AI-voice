<script setup lang="ts">
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="home-container">
    <header class="header">
      <h1>AI Voice Dashboard</h1>
      <button @click="authStore.logout()" class="logout-btn">Logout</button>
    </header>
    
    <main class="main-content">
      <h2>Welcome to AI Voice</h2>
      <p>This is a placeholder dashboard. Your AI voice application content will appear here.</p>
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
