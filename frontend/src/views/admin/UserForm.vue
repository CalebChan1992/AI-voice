<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { userService, organizationService } from '../../services/api'

const router = useRouter()
const route = useRoute()
const userId = computed(() => route.params.id ? parseInt(route.params.id as string) : null)
const isEditMode = computed(() => !!userId.value)
const pageTitle = computed(() => isEditMode.value ? 'Edit User' : 'Create User')

const loading = ref(false)
const saving = ref(false)
const error = ref('')
const organizations = ref([])

// Form data
const form = reactive({
  username: '',
  password: '',
  email: '',
  first_name: '',
  last_name: '',
  role: 'user',
  is_active: true,
  organization_id: null as number | null
})

// Available roles
const roles = [
  { value: 'admin', label: 'Admin' },
  { value: 'manager', label: 'Manager' },
  { value: 'user', label: 'User' },
  { value: 'guest', label: 'Guest' }
]

// Fetch organizations
const fetchOrganizations = async () => {
  try {
    const response = await organizationService.getOrganizations()
    organizations.value = response.data.organizations
    
    // Set default organization if creating a new user
    if (!isEditMode.value && organizations.value.length > 0) {
      form.organization_id = organizations.value[0].id
    }
  } catch (err: any) {
    console.error('Error fetching organizations:', err)
  }
}

// Fetch user data if in edit mode
const fetchUserData = async () => {
  if (!isEditMode.value) return
  
  loading.value = true
  error.value = ''
  
  try {
    const response = await userService.getUserById(userId.value as number)
    const userData = response.data
    
    // Populate form with user data
    form.username = userData.username
    form.email = userData.email || ''
    form.first_name = userData.first_name || ''
    form.last_name = userData.last_name || ''
    form.role = userData.role
    form.is_active = userData.is_active !== false // Default to true if undefined
    form.organization_id = userData.organization_id
    
    // Clear password field in edit mode
    form.password = ''
  } catch (err: any) {
    error.value = err.response?.data?.msg || 'Failed to load user data'
    console.error('Error fetching user:', err)
  } finally {
    loading.value = false
  }
}

// Save user
const saveUser = async () => {
  saving.value = true
  error.value = ''
  
  try {
    if (isEditMode.value) {
      // Update existing user
      const updateData = { ...form }
      
      // Only include password if it was provided
      if (!updateData.password) {
        delete updateData.password
      }
      
      await userService.updateUser(userId.value as number, updateData)
    } else {
      // Create new user
      await userService.createUser(form)
    }
    
    // Navigate back to user list
    router.push({ name: 'admin-users' })
  } catch (err: any) {
    error.value = err.response?.data?.msg || 'Failed to save user'
    console.error('Error saving user:', err)
  } finally {
    saving.value = false
  }
}

// Cancel and go back to user list
const cancel = () => {
  router.push({ name: 'admin-users' })
}

// Load data when component is mounted
onMounted(async () => {
  await fetchOrganizations()
  await fetchUserData()
})
</script>

<template>
  <div class="user-form">
    <div class="form-header">
      <h2 class="section-title">{{ pageTitle }}</h2>
    </div>
    
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="loading" class="loading">Loading user data...</div>
    
    <form v-else @submit.prevent="saveUser" class="form-container">
      <div class="form-group">
        <label for="username" class="form-label">Username *</label>
        <input
          id="username"
          v-model="form.username"
          type="text"
          class="form-input"
          required
          :disabled="isEditMode"
        />
      </div>
      
      <div class="form-group">
        <label for="password" class="form-label">
          {{ isEditMode ? 'Password (leave blank to keep current)' : 'Password *' }}
        </label>
        <input
          id="password"
          v-model="form.password"
          type="password"
          class="form-input"
          :required="!isEditMode"
        />
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="first_name" class="form-label">First Name</label>
          <input
            id="first_name"
            v-model="form.first_name"
            type="text"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="last_name" class="form-label">Last Name</label>
          <input
            id="last_name"
            v-model="form.last_name"
            type="text"
            class="form-input"
          />
        </div>
      </div>
      
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          class="form-input"
        />
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="role" class="form-label">Role *</label>
          <select
            id="role"
            v-model="form.role"
            class="form-select"
            required
          >
            <option v-for="role in roles" :key="role.value" :value="role.value">
              {{ role.label }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="organization" class="form-label">Organization</label>
          <select
            id="organization"
            v-model="form.organization_id"
            class="form-select"
          >
            <option :value="null">None</option>
            <option v-for="org in organizations" :key="org.id" :value="org.id">
              {{ org.name }} ({{ org.plan }})
            </option>
          </select>
        </div>
      </div>
      
      <div class="form-group checkbox-group">
        <label class="checkbox-label">
          <input
            type="checkbox"
            v-model="form.is_active"
          />
          <span>Active</span>
        </label>
      </div>
      
      <div class="form-actions">
        <button type="button" class="btn-secondary" @click="cancel">
          Cancel
        </button>
        <button type="submit" class="btn-primary" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save User' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.user-form {
  width: 100%;
}

.form-header {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.error-message {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
}

.loading {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
}

.form-input, .form-select {
  padding: 0.625rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #1f2937;
  background-color: white;
}

.form-input:focus, .form-select:focus {
  outline: none;
  border-color: #41B883;
  box-shadow: 0 0 0 2px rgba(65, 184, 131, 0.2);
}

.checkbox-group {
  margin-top: 0.5rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary, .btn-secondary {
  padding: 0.625rem 1.25rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #41B883;
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: #369e6f;
}

.btn-primary:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: white;
  color: #4b5563;
  border: 1px solid #d1d5db;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
}
</style>
