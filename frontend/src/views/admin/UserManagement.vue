<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userService } from '../../services/api'
import {
  PencilIcon,
  TrashIcon,
  PlusCircleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const users = ref([])
const loading = ref(true)
const error = ref('')

// Fetch all users
const fetchUsers = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await userService.getUsers()
    users.value = response.data.users
  } catch (err: any) {
    error.value = err.response?.data?.msg || 'Failed to load users'
    console.error('Error fetching users:', err)
  } finally {
    loading.value = false
  }
}

// Delete a user
const deleteUser = async (userId: number) => {
  if (!confirm('Are you sure you want to delete this user?')) return
  
  try {
    await userService.deleteUser(userId)
    // Refresh the user list
    fetchUsers()
  } catch (err: any) {
    error.value = err.response?.data?.msg || 'Failed to delete user'
    console.error('Error deleting user:', err)
  }
}

// Navigate to create user form
const goToCreateUser = () => {
  router.push({ name: 'admin-users-create' })
}

// Navigate to edit user form
const goToEditUser = (userId: number) => {
  router.push({ name: 'admin-users-edit', params: { id: userId } })
}

// Get role badge class based on role
const getRoleBadgeClass = (role: string) => {
  switch (role) {
    case 'admin':
      return 'badge-admin'
    case 'manager':
      return 'badge-manager'
    case 'user':
      return 'badge-user'
    default:
      return 'badge-default'
  }
}

// Load users when component is mounted
onMounted(fetchUsers)
</script>

<template>
  <div class="user-management">
    <div class="header-actions">
      <h2 class="section-title">User Management</h2>
      <button class="btn-primary" @click="goToCreateUser">
        <PlusCircleIcon class="btn-icon" />
        Add User
      </button>
    </div>
    
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="loading" class="loading">Loading users...</div>
    
    <div v-else-if="users.length === 0" class="empty-state">
      No users found. Click "Add User" to create one.
    </div>
    
    <div v-else class="users-table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.first_name }} {{ user.last_name }}</td>
            <td>{{ user.email || '-' }}</td>
            <td>
              <span class="role-badge" :class="getRoleBadgeClass(user.role)">
                {{ user.role }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="btn-icon-action" @click="goToEditUser(user.id)" title="Edit user">
                <PencilIcon class="action-icon" />
              </button>
              <button class="btn-icon-action btn-danger" @click="deleteUser(user.id)" title="Delete user">
                <TrashIcon class="action-icon" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.user-management {
  width: 100%;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #41B883;
  color: white;
  border: none;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #369e6f;
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.error-message {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}

.loading, .empty-state {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.users-table-container {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th, .users-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.users-table th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #4b5563;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-admin {
  background-color: #dbeafe;
  color: #1e40af;
}

.badge-manager {
  background-color: #e0e7ff;
  color: #4338ca;
}

.badge-user {
  background-color: #d1fae5;
  color: #065f46;
}

.badge-default {
  background-color: #f3f4f6;
  color: #4b5563;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background-color: #d1fae5;
  color: #065f46;
}

.status-inactive {
  background-color: #fee2e2;
  color: #b91c1c;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.btn-icon-action {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f3f4f6;
  border: none;
  border-radius: 0.375rem;
  width: 2rem;
  height: 2rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-icon-action:hover {
  background-color: #e5e7eb;
}

.btn-danger:hover {
  background-color: #fee2e2;
}

.action-icon {
  width: 1rem;
  height: 1rem;
  color: #4b5563;
}

.btn-danger .action-icon {
  color: #b91c1c;
}
</style>
