// Frontend test setup file
import { afterEach, beforeEach } from 'vitest'
import { createPinia } from 'pinia'

// Global setup for tests
beforeEach(() => {
  // Create a fresh Pinia instance for each test
  const pinia = createPinia()
  // You can add more global setup here
})

afterEach(() => {
  // Clean up after each test
})
