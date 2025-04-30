<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { organizationService } from '../../services/api'

const organizations = ref([])
const loading = ref(true)
const error = ref('')

// Fetch all organizations
const fetchOrganizations = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await organizationService.getOrganizations()
    organizations.value = response.data.organizations
  } catch (err: any) {
    error.value = err.response?.data?.msg || 'Failed to load organizations'
    console.error('Error fetching organizations:', err)
  } finally {
    loading.value = false
  }
}

// Format date
const formatDate = (dateString: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString()
}

// Load organizations when component is mounted
onMounted(fetchOrganizations)
</script>

<template>
  <div class="organization-management">
    <div class="header-actions">
      <h2 class="section-title">Organization Management</h2>
    </div>
    
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div v-if="loading" class="loading">Loading organizations...</div>
    
    <div v-else-if="organizations.length === 0" class="empty-state">
      No organizations found.
    </div>
    
    <div v-else class="organizations-table-container">
      <table class="organizations-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Plan</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="org in organizations" :key="org.id">
            <td>{{ org.id }}</td>
            <td>{{ org.name }}</td>
            <td>
              <span class="plan-badge" :class="`plan-${org.plan}`">
                {{ org.plan }}
              </span>
            </td>
            <td>{{ formatDate(org.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.organization-management {
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

.organizations-table-container {
  overflow-x: auto;
}

.organizations-table {
  width: 100%;
  border-collapse: collapse;
}

.organizations-table th, .organizations-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.organizations-table th {
  background-color: #f9fafb;
  font-weight: 600;
  color: #4b5563;
}

.plan-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.plan-free {
  background-color: #e0e7ff;
  color: #4338ca;
}

.plan-basic {
  background-color: #d1fae5;
  color: #065f46;
}

.plan-premium {
  background-color: #fef3c7;
  color: #92400e;
}

.plan-enterprise {
  background-color: #dbeafe;
  color: #1e40af;
}
</style>
