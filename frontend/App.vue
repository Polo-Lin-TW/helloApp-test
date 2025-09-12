<template>
  <div id="app">
    <header>
      <h1>{{ title }}</h1>
      <p class="subtitle">{{ subtitle }}</p>
    </header>

    <main>
      <!-- Basic Hello World Section -->
      <section class="card">
        <h2>Basic Hello World</h2>
        <p>{{ localMessage }}</p>
        <button @click="updateLocalMessage" class="btn btn-primary">
          Change Message
        </button>
      </section>

      <!-- API Integration Section -->
      <section class="card">
        <h2>FastAPI Integration</h2>
        <div class="input-group">
          <input 
            v-model="userName" 
            type="text" 
            placeholder="Enter your name (optional)"
            class="input"
          >
          <button @click="fetchFromAPI" class="btn btn-secondary" :disabled="loading">
            {{ loading ? 'Loading...' : 'Get Message from API' }}
          </button>
        </div>
        
        <div v-if="apiResponse" class="api-response">
          <h3>API Response:</h3>
          <div class="response-content">
            <p><strong>Message:</strong> {{ apiResponse.message }}</p>
            <p><strong>Timestamp:</strong> {{ formatTimestamp(apiResponse.timestamp) }}</p>
            <p><strong>Backend:</strong> {{ apiResponse.backend }}</p>
            <p><strong>Frontend:</strong> {{ apiResponse.frontend }}</p>
          </div>
        </div>

        <div v-if="error" class="error">
          <p><strong>Error:</strong> {{ error }}</p>
        </div>
      </section>

      <!-- Counter Demo Section -->
      <section class="card">
        <h2>Interactive Counter</h2>
        <div class="counter">
          <button @click="decrementCounter" class="btn btn-outline">-</button>
          <span class="counter-value">{{ counter }}</span>
          <button @click="incrementCounter" class="btn btn-outline">+</button>
        </div>
        <button @click="resetCounter" class="btn btn-small">Reset</button>
      </section>

      <!-- Status Section -->
      <section class="card">
        <h2>System Status</h2>
        <div class="status-grid">
          <div class="status-item">
            <span class="status-label">Frontend:</span>
            <span class="status-value online">Vue 3.js ✓</span>
          </div>
          <div class="status-item">
            <span class="status-label">Backend:</span>
            <span class="status-value" :class="backendStatus">
              FastAPI {{ backendStatus === 'online' ? '✓' : '✗' }}
            </span>
          </div>
        </div>
        <button @click="checkBackendHealth" class="btn btn-small">Check Backend</button>
      </section>
    </main>

    <footer>
      <p>Built with Vue 3.js + FastAPI | Demo Application</p>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    // Reactive data
    const title = ref('Hello World Web App')
    const subtitle = ref('Vue 3.js Frontend + FastAPI Backend')
    const localMessage = ref('Hello, World! This is Vue 3.js in action!')
    const userName = ref('')
    const apiResponse = ref(null)
    const error = ref(null)
    const loading = ref(false)
    const counter = ref(0)
    const backendStatus = ref('unknown')
    const apiBaseUrl = ref('')

    // Methods
    const updateLocalMessage = () => {
      const messages = [
        'Hello, World! This is Vue 3.js in action!',
        'Vue 3 is awesome! 🚀',
        'Reactive programming made easy!',
        'Building modern web apps with Vue 3!',
        'Hello from the frontend! 👋'
      ]
      const currentIndex = messages.indexOf(localMessage.value)
      const nextIndex = (currentIndex + 1) % messages.length
      localMessage.value = messages[nextIndex]
    }

    const fetchFromAPI = async () => {
      loading.value = true
      error.value = null
      apiResponse.value = null

      try {
        const url = userName.value 
          ? `${apiBaseUrl.value}/api/message?name=${encodeURIComponent(userName.value)}`
          : `${apiBaseUrl.value}/api/message`
        
        logInfo('Attempting to fetch data from backend API', {
          url,
          userName: userName.value || 'anonymous',
          backendUrl: apiBaseUrl.value
        })
        
        const response = await axios.get(url, {
          timeout: 10000 // 10 second timeout
        })
        
        apiResponse.value = response.data
        backendStatus.value = 'online'
        
        logConnection('success', {
          url,
          status: response.status,
          statusText: response.statusText,
          responseData: response.data
        })
        
      } catch (err) {
        error.value = `Failed to connect to backend: ${err.message}`
        backendStatus.value = 'offline'
        
        logConnection('failed', {
          url: `${apiBaseUrl.value}/api/message`,
          error: err.message,
          code: err.code,
          response: err.response ? {
            status: err.response.status,
            statusText: err.response.statusText,
            data: err.response.data
          } : null
        })
        
        logError('API request failed', err)
      } finally {
        loading.value = false
      }
    }

    const checkBackendHealth = async () => {
      try {
        const healthUrl = `${apiBaseUrl.value}/health`
        logInfo('Checking backend health', { healthUrl })
        
        const response = await axios.get(healthUrl, {
          timeout: 5000 // 5 second timeout for health check
        })
        
        if (response.data.status === 'healthy') {
          backendStatus.value = 'online'
          logConnection('success', {
            type: 'health_check',
            url: healthUrl,
            status: response.status,
            healthStatus: response.data.status,
            responseData: response.data
          })
        } else {
          backendStatus.value = 'offline'
          logInfo('Backend health check returned unhealthy status', {
            url: healthUrl,
            responseData: response.data
          })
        }
      } catch (err) {
        backendStatus.value = 'offline'
        logConnection('failed', {
          type: 'health_check',
          url: `${apiBaseUrl.value}/health`,
          error: err.message,
          code: err.code,
          response: err.response ? {
            status: err.response.status,
            statusText: err.response.statusText,
            data: err.response.data
          } : null
        })
        logError('Health check failed', err)
      }
    }

    const incrementCounter = () => {
      counter.value++
    }

    const decrementCounter = () => {
      counter.value--
    }

    const resetCounter = () => {
      counter.value = 0
    }

    const formatTimestamp = (timestamp) => {
      return new Date(timestamp).toLocaleString()
    }

    // Logging utility functions
    const logInfo = (message, data = {}) => {
      const timestamp = new Date().toISOString()
      console.log(`[FRONTEND ${timestamp}] INFO: ${message}`, data)
    }

    const logError = (message, error = {}) => {
      const timestamp = new Date().toISOString()
      console.error(`[FRONTEND ${timestamp}] ERROR: ${message}`, error)
    }

    const logConnection = (status, details = {}) => {
      const timestamp = new Date().toISOString()
      const statusMsg = status === 'success' ? 'SUCCESS' : 'FAILED'
      console.log(`[FRONTEND ${timestamp}] BACKEND_CONNECTION_${statusMsg}:`, details)
    }

    // Enhanced backend configuration with logging
    const initializeBackendConfig = () => {
      // Try to determine backend URL from environment or use defaults
      const backendHost = import.meta.env.VITE_BACKEND_HOST || 'helloapp_backend'
      const backendPort = import.meta.env.VITE_BACKEND_PORT || '8000'
      
      // For development, use localhost if we're in dev mode
      if (import.meta.env.DEV) {
        apiBaseUrl.value = `http://localhost:${backendPort}`
        logInfo('Development mode detected, using localhost for backend connection', {
          backendUrl: apiBaseUrl.value
        })
      } else {
        apiBaseUrl.value = `http://${backendHost}:${backendPort}`
        logInfo('Production mode, using container names for backend connection', {
          backendHost,
          backendPort,
          backendUrl: apiBaseUrl.value
        })
      }
    }

    // Lifecycle hooks
    onMounted(() => {
      logInfo('Frontend component mounted, initializing backend connection')
      
      // Initialize backend configuration
      initializeBackendConfig()
      
      // Check backend health on component mount
      logInfo('Starting backend health check')
      checkBackendHealth()
      
      // Auto-fetch a welcome message
      logInfo('Scheduling automatic API fetch in 1 second')
      setTimeout(() => {
        fetchFromAPI()
      }, 1000)
    })

    // Return reactive data and methods
    return {
      title,
      subtitle,
      localMessage,
      userName,
      apiResponse,
      error,
      loading,
      counter,
      backendStatus,
      apiBaseUrl,
      updateLocalMessage,
      fetchFromAPI,
      checkBackendHealth,
      incrementCounter,
      decrementCounter,
      resetCounter,
      formatTimestamp
    }
  }
}
</script>

<style scoped>
/* Reset and base styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
header {
  text-align: center;
  margin-bottom: 40px;
  color: white;
}

header h1 {
  font-size: 3rem;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
}

/* Main content */
main {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

/* Card component */
.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card h2 {
  color: #4a5568;
  margin-bottom: 16px;
  font-size: 1.5rem;
}

/* Buttons */
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4);
}

.btn-outline {
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.btn-small {
  padding: 8px 16px;
  font-size: 0.9rem;
  background: #e2e8f0;
  color: #4a5568;
}

.btn-small:hover {
  background: #cbd5e0;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Input styles */
.input-group {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.input {
  flex: 1;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  min-width: 200px;
}

.input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* API Response */
.api-response {
  background: #f7fafc;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
  border-left: 4px solid #48bb78;
}

.api-response h3 {
  color: #2d3748;
  margin-bottom: 12px;
}

.response-content p {
  margin-bottom: 8px;
}

.response-content strong {
  color: #4a5568;
}

/* Error styles */
.error {
  background: #fed7d7;
  border: 1px solid #feb2b2;
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
  color: #c53030;
}

/* Counter */
.counter {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.counter-value {
  font-size: 2rem;
  font-weight: bold;
  color: #4a5568;
  min-width: 60px;
  text-align: center;
}

/* Status */
.status-grid {
  display: grid;
  gap: 12px;
  margin-bottom: 16px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.status-label {
  font-weight: 600;
  color: #4a5568;
}

.status-value {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.status-value.online {
  background: #c6f6d5;
  color: #22543d;
}

.status-value.offline {
  background: #fed7d7;
  color: #c53030;
}

.status-value.unknown {
  background: #e2e8f0;
  color: #4a5568;
}

/* Footer */
footer {
  text-align: center;
  color: white;
  opacity: 0.8;
  padding: 20px 0;
}

/* Responsive design */
@media (max-width: 768px) {
  #app {
    padding: 10px;
  }
  
  header h1 {
    font-size: 2rem;
  }
  
  main {
    grid-template-columns: 1fr;
  }
  
  .input-group {
    flex-direction: column;
  }
  
  .input {
    min-width: auto;
  }
  
  .counter {
    gap: 15px;
  }
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  animation: fadeIn 0.6s ease-out;
}

.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
</style>