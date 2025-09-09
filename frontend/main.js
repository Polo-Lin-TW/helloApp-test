import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

// Make axios available globally
const app = createApp(App)

// Add axios to global properties (optional)
app.config.globalProperties.$axios = axios

// Mount the app
app.mount('#app')