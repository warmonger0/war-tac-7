/**
 * Application configuration
 */

// API Base URL configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Frontend configuration
export const FRONTEND_PORT = import.meta.env.VITE_PORT || '5173';

// Feature flags
export const FEATURES = {
  webBuilder: true,
  sqlInterface: true,
  darkMode: false,
};

// UI Configuration
export const UI_CONFIG = {
  maxQueryLength: 5000,
  maxFileSize: 10 * 1024 * 1024, // 10MB
  debounceDelay: 400,
};