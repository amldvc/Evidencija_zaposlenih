<template>
  <nav class="navbar">
    <!-- Zlatna traka samo na login ruti -->
    <div v-if="$route.name === 'login'" style="background-color: #D4AF37; height: 50px;">
      <!-- Prazna traka u zlatnoj boji -->
    </div>

    <!-- Navbar za menadžer rutu (izvorni navbar sa svim linkovima) -->
    <div v-if="$route.name === 'menadzer'" class="nav-container">
      <ul class="logo">MENADŽER</ul>
      <ul class="nav-links">
        <li><router-link to="/zaposleni">ZAPOSLENI</router-link></li>
        <li><router-link to="/radnik_raspored">RASPORED RADNIKA</router-link></li>
        <li><router-link to="/izmena_rasporeda">IZMENA RASPOREDA</router-link></li>
      </ul>
      <a href="#" @click.prevent="logout" class="logout-btn">
        <i class="fas fa-sign-out-alt"></i>
      </a>
    </div>

    <!-- Navbar za zaposleni, radnik_raspored i izmena_rasporeda rute (samo dugme za odjavu) -->
    <div v-if="$route.name === 'zaposleni' || $route.name === 'radnik_raspored' || $route.name === 'izmena_rasporeda'" class="nav-container">
      <div class="nav-links">
        <a href="#" @click.prevent="logout" class="logout-btn">
          <i class="fas fa-sign-out-alt"></i>
        </a>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  methods: {
    async logout() {
      try {
        await axios.post("http://localhost:5000/api/logout");
        localStorage.removeItem("token");
        this.$router.push("/");
      } catch (error) {
        console.error("Greška pri odjavi:", error);
      }
    }
  }
};
</script>

<style scoped>
.navbar {
  width: 100%; /* Širina navbar-a je 100% širine ekrana */
  display: flex; /* Postavlja navbar kao fleks konteiner */
  flex-direction: column; /* Poređuje elemente u koloni */
}

/* Stilizuje kontejner unutar navbara */
.nav-container {
  display: flex; /* Postavlja kontejner kao fleks konteiner */
  justify-content: center; /* Centriranje svih elemenata horizontalno */
  align-items: center; /* Centriranje svih elemenata vertikalno */
  padding: 10px 20px; /* Dodaje unutrašnji razmak sa svih strana */
}

/* Stil za logo, koji je jednostavan tekst */
.logo {
  font-size: 1.5rem; /* Veliki font za logo */
  font-weight: bold; /* Logo tekst je podebljan */
}

/* Stil za listu linkova u navbaru */
.nav-links {
  display: flex; /* Postavlja listu linkova kao fleks kontejner */
  gap: 15px; /* Dodaje razmak između linkova */
}

/* Stil za pojedinačne linkove u navbaru */
.nav-links a {
  text-decoration: none; /* Uklanja podvlačenje sa linkova */
  color: white; /* Podesi boju teksta na belu */
  font-size: 1rem; /* Podesi veličinu fonta */
}

/* Stil za dugme za odjavu */
.logout-btn {
  font-size: 2rem; /* Veći font za dugme za odjavu */
  cursor: pointer; /* Promeni kursor u pokazivač kada se pređe preko dugmeta */
}

/* Stil za ikonu u dugmetu za odjavu */
.logout-btn i {
  color: #B8860B; /* Postavlja boju ikone na tamno zlatnu */
}
</style scoped>

