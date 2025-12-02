import { Configuration, HealthApi } from '@technight/api';

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:6173';

// Create API Configuration
const apiConfig = new Configuration({
  basePath: API_BASE_URL
});

// Export configured API clients
export const healthApi = new HealthApi(apiConfig);

// Export configuration for advanced usage
export { apiConfig, API_BASE_URL };
