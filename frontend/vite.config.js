import { cwd } from 'node:process'
import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const { VITE_API_URL } = loadEnv(mode, cwd(), 'VITE_')
  if (!VITE_API_URL?.trim()) {
    throw new Error('Configura VITE_API_URL en frontend/.env o en el entorno de compilación.')
  }

  let apiUrl
  try {
    apiUrl = new URL(VITE_API_URL.trim())
  } catch {
    throw new Error('VITE_API_URL debe ser una URL absoluta con http o https.')
  }

  if (
    !['http:', 'https:'].includes(apiUrl.protocol) ||
    apiUrl.username || apiUrl.password || apiUrl.search || apiUrl.hash
  ) {
    throw new Error('VITE_API_URL debe usar http o https, sin credenciales, parámetros ni fragmentos.')
  }

  return {
    plugins: [react()],
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(apiUrl.toString().replace(/\/+$/, '')),
    },
  }
})
