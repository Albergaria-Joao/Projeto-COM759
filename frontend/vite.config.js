import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 8080, // AQUI: Força o Vite a rodar na porta 8080
    strictPort: true, // Garante que se a 8080 estiver ocupada, ele avisa e não muda de porta
    proxy: {
      // Configuração de Proxy do Vite (diferente do Vue CLI)
      '/login': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/logout': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/get-tarefas': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/create-tarefa': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/update-status-tarefa': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/delete-tarefa': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/get-equipes': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/get-membros': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false },
      '/me': { target: 'http://127.0.0.1:5000', changeOrigin: true, secure: false }
    }
  }
})