import './assets/main.css';
import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap';
import router from './router/index';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { createHead } from '@vueuse/head';
import axios from 'axios';
import { API_BASE_URL } from './scripts/Constants';

// Configure axios for different environments
// In development: /api/* → Vite proxy strips /api → https://...net/*
// In production: /api/* → https://...net/* (strip /api prefix)
if (import.meta.env.PROD) {
  axios.defaults.baseURL = API_BASE_URL;
  
  // Add request interceptor to strip /api prefix in production
  axios.interceptors.request.use((config) => {
    if (config.url && config.url.startsWith('/api')) {
      config.url = config.url.replace(/^\/api/, '');
    }
    return config;
  });
}

const app = createApp(App);
app.use(createHead());
app.use(router);

app.mount('#app');

