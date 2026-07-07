import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendUrl = env.VITE_API_URL || 'http://localhost:8000'

  return {
    plugins: [react()],
    server: {
      port: 3000,
      strictPort: false,
      proxy: {
        '/api': {
          target: backendUrl,
          changeOrigin: true,
          secure: false,
        },
      },
    },
    build: {
      outDir: 'dist',
      sourcemap: false,
      chunkSizeWarningLimit: 2500,
      rollupOptions: {
        output: {
          manualChunks: {
            react:   ['react', 'react-dom'],
            motion:  ['framer-motion'],
            echarts: ['echarts'],
            icons:   ['lucide-react'],
          },
        },
      },
    },
    define: { global: 'globalThis' },
    optimizeDeps: {
      include: ['echarts', 'framer-motion', 'lucide-react', 'zustand'],
    },
  }
})
