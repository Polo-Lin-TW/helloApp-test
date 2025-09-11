import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => ({
  plugins: [vue()],
  server: {
    port: 3000,
    host: true,
    cors: true
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    minify: mode === 'production',
    sourcemap: mode === 'development',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue'],
          // 如果使用其他套件，可以分離
          // utils: ['lodash', 'axios']
        }
      }
    }
  }
}))