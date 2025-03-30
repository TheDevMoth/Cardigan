import './assets/main.css';
import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap';
import router from './router/index';
import 'bootstrap-icons/font/bootstrap-icons.css';
import { createHead } from '@vueuse/head';

const app = createApp(App);
app.use(createHead());
app.use(router);

app.mount('#app');

