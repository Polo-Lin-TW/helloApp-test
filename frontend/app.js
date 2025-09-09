const { createApp } = Vue;

createApp({
    data() {
        return {
            title: 'Hello World Web App',
            subtitle: 'Vue 3.js Frontend + FastAPI Backend',
            localMessage: 'Hello, World! This is Vue 3.js in action!',
            userName: '',
            apiResponse: null,
            error: null,
            loading: false,
            counter: 0,
            backendStatus: 'unknown',
            apiBaseUrl: 'http://localhost:8000'
        }
    },
    methods: {
        updateLocalMessage() {
            const messages = [
                'Hello, World! This is Vue 3.js in action!',
                'Vue 3 is awesome! 🚀',
                'Reactive programming made easy!',
                'Building modern web apps with Vue 3!',
                'Hello from the frontend! 👋'
            ];
            const currentIndex = messages.indexOf(this.localMessage);
            const nextIndex = (currentIndex + 1) % messages.length;
            this.localMessage = messages[nextIndex];
        },

        async fetchFromAPI() {
            this.loading = true;
            this.error = null;
            this.apiResponse = null;

            try {
                const url = this.userName 
                    ? `${this.apiBaseUrl}/api/message?name=${encodeURIComponent(this.userName)}`
                    : `${this.apiBaseUrl}/api/message`;
                
                const response = await axios.get(url);
                this.apiResponse = response.data;
                this.backendStatus = 'online';
            } catch (err) {
                this.error = `Failed to connect to backend: ${err.message}`;
                this.backendStatus = 'offline';
                console.error('API Error:', err);
            } finally {
                this.loading = false;
            }
        },

        async checkBackendHealth() {
            try {
                const response = await axios.get(`${this.apiBaseUrl}/health`);
                if (response.data.status === 'healthy') {
                    this.backendStatus = 'online';
                } else {
                    this.backendStatus = 'offline';
                }
            } catch (err) {
                this.backendStatus = 'offline';
                console.error('Health check failed:', err);
            }
        },

        incrementCounter() {
            this.counter++;
        },

        decrementCounter() {
            this.counter--;
        },

        resetCounter() {
            this.counter = 0;
        },

        formatTimestamp(timestamp) {
            return new Date(timestamp).toLocaleString();
        }
    },

    mounted() {
        // Check backend health on component mount
        this.checkBackendHealth();
        
        // Auto-fetch a welcome message
        setTimeout(() => {
            this.fetchFromAPI();
        }, 1000);
    }
}).mount('#app');