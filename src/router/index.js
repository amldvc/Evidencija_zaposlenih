import { createRouter, createWebHistory } from 'vue-router';

// Uvozimo komponente
import login from '../views/login.vue';
import zaposleni from '../views/zaposleni.vue';
import menadzer from '../views/menadzer.vue';
import radnik_raspored from '../views/radnik_raspored.vue';
import izmena_rasporeda from '../views/izmena_rasporeda.vue';

const routes = [
  { path: '/', redirect: '/login' }, // Ako korisnik otvori "/", preusmerava se na login
  { path: '/login', name: 'login', component: login },  
  { path: '/zaposleni', name: 'zaposleni', component: zaposleni },
  { path: '/menadzer', name: 'menadzer', component: menadzer },
  { path: '/radnik_raspored', name: 'radnik_raspored', component: radnik_raspored },
  { path: '/izmena_rasporeda', name: 'izmena_rasporeda', component: izmena_rasporeda },
  { path: '/:pathMatch(.*)*', redirect: '/login' } // Ako korisnik unese nepostojeću rutu, preusmerava se na login
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

export default router;
