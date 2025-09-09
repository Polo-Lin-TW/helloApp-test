# Vue 3 SFC Migration Guide

This document describes the migration from traditional Vue 3 setup to Single File Components (SFC) architecture.

## What Changed

### Before (Traditional Setup)
```
frontend/
├── index.html    # Full HTML template with Vue directives
├── app.js        # Vue application with Options API
└── style.css     # Global styles
```

### After (SFC Setup)
```
frontend/
├── index.html       # Minimal HTML entry point
├── App.vue          # Single File Component with template, script, style
├── main.js          # Vue application bootstrap
├── package.json     # Node.js dependencies
├── vite.config.js   # Vite build configuration
├── app.js.backup    # Backup of original app.js
└── style.css.backup # Backup of original styles
```

## Key Improvements

### 1. Single File Components (SFC)
- **Template**: HTML template in `<template>` section
- **Script**: JavaScript logic in `<script>` section using Composition API
- **Style**: CSS styles in `<style scoped>` section

### 2. Composition API
- Uses `setup()` function instead of Options API
- Reactive data with `ref()` and `reactive()`
- Better TypeScript support
- More logical code organization

### 3. Modern Build Tools
- **Vite**: Fast development server with Hot Module Replacement (HMR)
- **ES Modules**: Native browser module support
- **Tree Shaking**: Optimized bundle size

### 4. Development Experience
- **Hot Reload**: Instant updates during development
- **Component Isolation**: Scoped styles prevent CSS conflicts
- **Better Debugging**: Vue DevTools integration
- **Modern JavaScript**: ES6+ features support

## Code Comparison

### Traditional Setup (app.js)
```javascript
const { createApp } = Vue;

createApp({
    data() {
        return {
            title: 'Hello World Web App',
            counter: 0
        }
    },
    methods: {
        increment() {
            this.counter++
        }
    }
}).mount('#app')
```

### SFC Setup (App.vue)
```vue
<template>
  <div>
    <h1>{{ title }}</h1>
    <button @click="increment">{{ counter }}</button>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const title = ref('Hello World Web App')
    const counter = ref(0)
    
    const increment = () => {
      counter.value++
    }
    
    return {
      title,
      counter,
      increment
    }
  }
}
</script>

<style scoped>
/* Component-specific styles */
</style>
```

## Development Workflow

### Option 1: Vite Development Server (Recommended)
```bash
cd frontend
npm install
npm run dev
```

**Benefits:**
- Hot Module Replacement (HMR)
- Fast build times
- Modern ES modules
- Optimized development experience

### Option 2: Python HTTP Server (Fallback)
```bash
cd frontend
python3 -m http.server 3000
```

**Benefits:**
- No Node.js dependency
- Simple setup
- Works with CDN Vue

## File Structure Details

### App.vue Structure
```vue
<template>
  <!-- HTML template with Vue directives -->
</template>

<script>
// Composition API setup
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    // Reactive data
    const message = ref('Hello World')
    
    // Methods
    const updateMessage = () => {
      message.value = 'Updated!'
    }
    
    // Lifecycle hooks
    onMounted(() => {
      console.log('Component mounted')
    })
    
    // Return reactive data and methods
    return {
      message,
      updateMessage
    }
  }
}
</script>

<style scoped>
/* Scoped styles - only apply to this component */
</style>
```

### main.js Bootstrap
```javascript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')
```

### package.json Scripts
```json
{
  "scripts": {
    "dev": "vite",           // Development server
    "build": "vite build",   // Production build
    "preview": "vite preview", // Preview production build
    "serve": "python3 -m http.server 3000" // Fallback server
  }
}
```

## Migration Benefits

1. **Better Code Organization**: Logic, template, and styles in one file
2. **Improved Performance**: Tree shaking and optimized builds
3. **Enhanced Developer Experience**: HMR, better debugging
4. **Modern Standards**: ES modules, Composition API
5. **Scalability**: Better for larger applications
6. **Component Reusability**: Easier to create reusable components

## Backward Compatibility

The original files are preserved as backups:
- `app.js.backup` - Original Vue application
- `style.css.backup` - Original global styles

You can still use the Python HTTP server method if Node.js is not available.

## Next Steps

1. **Install Node.js** for optimal development experience
2. **Use Vite** for development (`npm run dev`)
3. **Create additional components** in separate `.vue` files
4. **Add routing** with Vue Router
5. **Add state management** with Pinia/Vuex
6. **Build for production** with `npm run build`

## Troubleshooting

### Common Issues

1. **Module not found errors**: Ensure all imports use correct paths
2. **CORS issues**: Make sure backend CORS is properly configured
3. **Hot reload not working**: Check Vite configuration
4. **Styles not applying**: Verify scoped styles syntax

### Debug Commands
```bash
# Check if Node.js is installed
node --version
npm --version

# Install dependencies
npm install

# Clear npm cache if needed
npm cache clean --force

# Run with verbose logging
npm run dev -- --debug
```