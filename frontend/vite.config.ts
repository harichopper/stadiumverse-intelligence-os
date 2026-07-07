import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: false,   // use next port if 3000 is busy
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      output: {
        manualChunks: {
          react:   ['react', 'react-dom'],
          motion:  ['framer-motion'],
          echarts: ['echarts', 'echarts-for-react'],
          router:  ['react-router-dom'],
          icons:   ['lucide-react'],
        },
      },
    },
  },
  define: { global: 'globalThis' },
  optimizeDeps: {
    include: ['echarts', 'framer-motion', 'lucide-react', 'zustand'],
  },
})
