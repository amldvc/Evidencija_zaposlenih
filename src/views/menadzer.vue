<script>
import axios from 'axios';

export default {
  data() {
    return {
      zaposleni: []
    };
  },
  async created() {
    try {
        const response = await axios.get('http://localhost:5000/api/menadzer', {
            withCredentials: true  // OBAVEZNO! Šalje kolačiće sesije
        });
        this.zaposleni = response.data.zaposleni;
    } catch (error) {
        console.error("Greška pri učitavanju podataka:", error);
        if (error.response && error.response.status === 401) {
            this.$router.push('/');  // Ako nije prijavljen, preusmeravamo ga na login
        }
    }
},
  methods: {
    async logout() {
    try {
        await axios.post("http://localhost:5000/api/logout");
        localStorage.removeItem("token"); // Ako koristiš token za autentifikaciju
        this.$router.push("/");  // Preusmeravanje na login
    } catch (error) {
        console.error("Greška pri odjavi:", error);
    }
}
  }
};
</script>

<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <ul class="logo">MENADŽER</ul>
        <ul class="nav-links">
          <li><router-link to="/zaposleni">ZAPOSLENI</router-link></li>
          <li><router-link to="/izmena_rasporeda">IZMENA RASPOREDA</router-link></li>
        </ul>
        <button class="logout-btn" @click="logout">
          <i class="fas fa-sign-out-alt"></i> 
        </button>
      </div>
    </nav>

    <div class="container">
      <h1>Dobrodošli, menadžeru!</h1>
    </div>
  </div>
</template>
