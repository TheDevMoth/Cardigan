import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap'
import router from './router/index';
import 'bootstrap-icons/font/bootstrap-icons.css'

const app = createApp(App);
app.use(router);

app.mount('#app');

