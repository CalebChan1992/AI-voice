<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
// Import Heroicons
import { UserIcon, LockClosedIcon, EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const isLoading = ref(false)
const errorMessage = ref('')
const showPassword = ref(false)

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleSubmit = async () => {
  if (!form.username || !form.password) {
    errorMessage.value = 'Please enter both username and password'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const success = await authStore.login(form.username, form.password)
    if (success) {
      router.push({ name: 'home' })
    } else {
      errorMessage.value = authStore.error || 'Login failed'
    }
  } catch (error: any) {
    errorMessage.value = error.message || 'An unexpected error occurred'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-content">
      <div class="login-left">
        <div class="login-form-container">
          <div class="logo-container">
            <h1 class="logo">AI VOICE</h1>
          </div>

          <form @submit.prevent="handleSubmit" class="login-form">
            <div class="form-group">
              <label for="username" class="visually-hidden">Username</label>
              <div class="input-with-icon">
                <UserIcon class="icon" />
                <input
                  type="text"
                  id="username"
                  v-model="form.username"
                  placeholder="Enter username"
                  autocomplete="username"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password" class="visually-hidden">Password</label>
              <div class="input-with-icon">
                <LockClosedIcon class="icon" />
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="password"
                  v-model="form.password"
                  placeholder="Enter password"
                  autocomplete="current-password"
                />
                <button
                  type="button"
                  class="password-toggle"
                  @click="togglePasswordVisibility"
                  aria-label="Toggle password visibility"
                >
                  <EyeIcon v-if="showPassword" class="eye-icon" />
                  <EyeSlashIcon v-else class="eye-icon" />
                </button>
              </div>
              <div class="forgot-password">
                <a href="#" @click.prevent>Forgot password?</a>
              </div>
            </div>

            <div class="form-group remember-me">
              <label class="checkbox-container">
                <input type="checkbox" v-model="form.rememberMe" />
                <span class="checkmark"></span>
                Remember me
              </label>
            </div>

            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>

            <button
              type="submit"
              class="login-button"
              :disabled="isLoading"
            >
              {{ isLoading ? 'Logging in...' : 'Login' }}
            </button>
          </form>

          <div class="language-selector">
            <!-- <span>English</span> | <span>Bahasa</span> | <span>Español</span> -->
             <span>English</span>
          </div>

          <!-- <div class="footer">
            <p>Service contact: support@aivoice.com</p>
            <p>© 2024 AI Voice</p>
          </div> -->
        </div>
      </div>

      <div class="login-right">
        <div class="ai-visual">
          <!-- AI-themed illustration -->
          <div class="ai-illustration">
            <div class="ai-core">AI</div>
            <div class="ai-node node-1"></div>
            <div class="ai-node node-2"></div>
            <div class="ai-node node-3"></div>
            <div class="ai-node node-4"></div>
            <div class="ai-connector connector-1"></div>
            <div class="ai-connector connector-2"></div>
            <div class="ai-connector connector-3"></div>
            <div class="ai-connector connector-4"></div>
            <div class="ai-wave"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Full page container */
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a6cff 0%, #0a9dff 100%);
  overflow: hidden;
  position: relative;
}

.login-container::after {
  content: '';
  position: absolute;
  bottom: -50px;
  left: 0;
  right: 0;
  height: 200px;
  background: #fff;
  border-radius: 100% 100% 0 0;
  z-index: 1;
}

.login-content {
  display: flex;
  width: 100%;
  height: 100%;
  z-index: 2;
}

/* Left side with login form */
.login-left {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.login-form-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 450px;
  padding: 2.5rem;
}

.logo-container {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  font-size: 2rem;
  font-weight: 700;
  color: #0a6cff;
  letter-spacing: 1px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  position: relative;
}

.input-with-icon {
  position: relative;
}

.icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  width: 20px;
  height: 20px;
}

.eye-icon {
  width: 20px;
  height: 20px;
  color: #6b7280;
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.password-toggle:hover .eye-icon {
  color: #0a6cff;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px 12px 12px 40px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

/* Add padding to the right for the password field to accommodate the eye icon */
#password {
  padding-right: 40px;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #0a6cff;
  outline: none;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.forgot-password {
  text-align: right;
  margin-top: 0.5rem;
}

.forgot-password a {
  color: #6b7280;
  font-size: 0.875rem;
  text-decoration: none;
}

.forgot-password a:hover {
  color: #0a6cff;
  text-decoration: underline;
}

.remember-me {
  display: flex;
  align-items: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.875rem;
  color: #6b7280;
}

.checkbox-container input {
  margin-right: 8px;
}

.error-message {
  color: #e94560;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.login-button {
  background-color: #0a6cff;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #0855cc;
}

.login-button:disabled {
  background-color: #93b8ff;
  cursor: not-allowed;
}

.language-selector {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  color: #6b7280;
}

.language-selector span {
  cursor: pointer;
  padding: 0 0.5rem;
}

.language-selector span:hover {
  color: #0a6cff;
}

.footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.75rem;
  color: #9ca3af;
}

/* Right side with AI visual */
.login-right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.ai-visual {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* AI Illustration */
.ai-illustration {
  position: relative;
  width: 400px;
  height: 400px;
}

.ai-core {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: #0a6cff;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2.5rem;
  font-weight: bold;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(10, 108, 255, 0.5);
  z-index: 2;
}

.ai-node {
  position: absolute;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.node-1 {
  top: 50px;
  left: 170px;
  background: linear-gradient(135deg, #64b5f6, #2196f3);
}

.node-2 {
  top: 170px;
  right: 50px;
  background: linear-gradient(135deg, #81c784, #4caf50);
}

.node-3 {
  bottom: 50px;
  left: 170px;
  background: linear-gradient(135deg, #e57373, #f44336);
}

.node-4 {
  top: 170px;
  left: 50px;
  background: linear-gradient(135deg, #ba68c8, #9c27b0);
}

.ai-connector {
  position: absolute;
  background: rgba(255, 255, 255, 0.7);
  z-index: 0;
}

.connector-1 {
  top: 100px;
  left: 195px;
  width: 10px;
  height: 70px;
}

.connector-2 {
  top: 195px;
  right: 100px;
  width: 70px;
  height: 10px;
}

.connector-3 {
  bottom: 100px;
  left: 195px;
  width: 10px;
  height: 70px;
}

.connector-4 {
  top: 195px;
  left: 100px;
  width: 70px;
  height: 10px;
}

.ai-wave {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  height: 300px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0.8;
  }
  50% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  100% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 0.8;
  }
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .login-content {
    flex-direction: column;
  }

  .login-right {
    display: none;
  }

  .login-left {
    width: 100%;
  }
}
</style>
