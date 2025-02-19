import { createApp } from 'vue'
import App from './App.vue'
import Vue3Toastify from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import router from './router'
import axios from 'axios';

const app = createApp(App)

app.use(Vue3Toastify,{
    autoClose: 3000,
});


// Axios postavke (ako su ti potrebne, npr. API url)
axios.defaults.baseURL = 'http://localhost:5000';  // Promeni na pravi URL tvog backenda
axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`;  // Ako koristiš autentifikaciju sa tokenom

app.config.globalProperties.$axios = axios;


app.use(router)
app.mount('#app')
