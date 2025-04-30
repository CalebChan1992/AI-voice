<script setup lang="ts">
import { ref } from 'vue'
import {
  BellIcon,
  UserCircleIcon,
  MagnifyingGlassIcon
} from '@heroicons/vue/24/solid'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <header class="header">
    <div class="header-container">

      <!-- Center section with search -->
      <div class="header-center">
        <div class="search-container">
          <MagnifyingGlassIcon class="search-icon" />
          <input type="text" placeholder="Search..." class="search-input" />
        </div>
      </div>

      <!-- Right section with user info and notifications -->
      <div class="header-right">
        <button class="icon-button">
          <BellIcon class="header-icon" />
        </button>
        <div class="user-info">
          <span v-if="authStore.user" class="username">
            {{ authStore.user.username }}
          </span>
          <UserCircleIcon class="user-icon" />
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.75rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 45;
  width: 100%;
  height: 64px; /* Fixed height to match sidebar header */
  display: flex;
  align-items: center;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-icon {
  width: 2rem;
  height: 2rem;
  color: #41B883; /* Vue green color */
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
}

.header-center {
  flex: 1;
  max-width: 500px;
  margin: 0 2rem;
  display: none;
}

@media (min-width: 768px) {
  .header-center {
    display: block;
  }
}

.search-container {
  position: relative;
  width: 100%;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: #6b7280;
}

.search-input {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #41B883;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.icon-button:hover {
  background-color: #f3f4f6;
}

.header-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #6b7280;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.username {
  font-size: 0.875rem;
  font-weight: 500;
  color: #2c3e50;
  display: none;
}

@media (min-width: 640px) {
  .username {
    display: inline;
  }
}

.user-icon {
  width: 2rem;
  height: 2rem;
  color: #6b7280;
}
</style>
