<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  ChartBarIcon, 
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ArrowsPointingOutIcon
} from '@heroicons/vue/24/solid'

// Props for the component
const props = defineProps<{
  title?: string;
  height?: number;
}>()

// Default values
const title = props.title || 'NPM Package Statistics'
const height = props.height || 300

// Sample data for the graph
const packageData = ref([
  { month: 'Jan', downloads: 1250 },
  { month: 'Feb', downloads: 1400 },
  { month: 'Mar', downloads: 1800 },
  { month: 'Apr', downloads: 1600 },
  { month: 'May', downloads: 2100 },
  { month: 'Jun', downloads: 2400 },
  { month: 'Jul', downloads: 2800 },
  { month: 'Aug', downloads: 3200 },
  { month: 'Sep', downloads: 3600 },
  { month: 'Oct', downloads: 4200 },
  { month: 'Nov', downloads: 4800 },
  { month: 'Dec', downloads: 5200 }
])

// Calculate max value for scaling
const maxDownloads = computed(() => {
  return Math.max(...packageData.value.map(item => item.downloads))
})

// Calculate percentage growth
const growthPercentage = computed(() => {
  const firstMonth = packageData.value[0].downloads
  const lastMonth = packageData.value[packageData.value.length - 1].downloads
  return Math.round(((lastMonth - firstMonth) / firstMonth) * 100)
})

// Calculate bar heights based on data
const calculateBarHeight = (downloads: number) => {
  const maxHeight = height - 60 // Subtract padding and labels height
  return (downloads / maxDownloads.value) * maxHeight
}

// Expand graph to full screen (placeholder function)
const expandGraph = () => {
  alert('Expand graph functionality would go here')
}

// Format number with commas
const formatNumber = (num: number) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}
</script>

<template>
  <div class="graph-widget">
    <div class="widget-header">
      <div class="widget-title">
        <ChartBarIcon class="widget-icon" />
        <h3>{{ title }}</h3>
      </div>
      <div class="widget-actions">
        <button class="action-button" @click="expandGraph">
          <ArrowsPointingOutIcon class="action-icon" />
        </button>
      </div>
    </div>
    
    <div class="widget-content">
      <div class="stats-summary">
        <div class="stat-item">
          <span class="stat-label">Total Downloads</span>
          <span class="stat-value">{{ formatNumber(packageData.reduce((sum, item) => sum + item.downloads, 0)) }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Growth</span>
          <div class="growth-indicator" :class="{ 'positive': growthPercentage > 0, 'negative': growthPercentage < 0 }">
            <ArrowTrendingUpIcon v-if="growthPercentage > 0" class="trend-icon" />
            <ArrowTrendingDownIcon v-else class="trend-icon" />
            <span>{{ growthPercentage }}%</span>
          </div>
        </div>
      </div>
      
      <div class="graph-container" :style="{ height: `${height}px` }">
        <div class="bar-chart">
          <div 
            v-for="(item, index) in packageData" 
            :key="index" 
            class="bar-container"
          >
            <div 
              class="bar" 
              :style="{ height: `${calculateBarHeight(item.downloads)}px` }"
              :title="`${item.month}: ${formatNumber(item.downloads)} downloads`"
            ></div>
            <div class="bar-label">{{ item.month }}</div>
          </div>
        </div>
        
        <!-- Y-axis labels -->
        <div class="y-axis">
          <div class="y-label">{{ formatNumber(maxDownloads) }}</div>
          <div class="y-label">{{ formatNumber(Math.round(maxDownloads / 2)) }}</div>
          <div class="y-label">0</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.graph-widget {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  width: 100%;
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.widget-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.widget-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #41B883; /* Vue green color */
}

.widget-title h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.widget-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.action-button:hover {
  background-color: #f3f4f6;
}

.action-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #6b7280;
}

.widget-content {
  position: relative;
}

.stats-summary {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
}

.growth-indicator {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.growth-indicator.positive {
  color: #10b981; /* Green */
}

.growth-indicator.negative {
  color: #ef4444; /* Red */
}

.trend-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.graph-container {
  position: relative;
  display: flex;
  align-items: flex-end;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  padding-bottom: 30px; /* Space for labels */
  padding-left: 40px; /* Space for y-axis */
}

.bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  height: 100%;
}

.bar {
  width: 80%;
  max-width: 30px;
  background-color: #41B883; /* Vue green color */
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease;
}

.bar:hover {
  background-color: #35495E; /* Vue dark color */
}

.bar-label {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.y-axis {
  position: absolute;
  left: 0;
  top: 0;
  height: calc(100% - 30px); /* Subtract label height */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.y-label {
  font-size: 0.75rem;
  color: #6b7280;
  transform: translateY(-50%);
}
</style>
