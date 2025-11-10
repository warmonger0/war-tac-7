// Global type definitions

// Environment variables (Vite)
interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_ENABLE_DEBUG: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// API types
export interface ApiResponse<T = unknown> {
  data: T
  message?: string
  error?: string
}

// Add your custom types here
