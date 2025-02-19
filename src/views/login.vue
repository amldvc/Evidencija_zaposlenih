<template>
  <div class="container">
    <img src="@/assets/images/logo.png" alt="Divine Beauty Logo" class="logo" />
    <form @submit.prevent="login">
      <h3>PRIJAVA</h3>
      <label for="email">EMAIL ADRESA</label>
      <input type="email" v-model="email" required />

      <label for="password">LOZINKA</label>
      <input type="password" v-model="password" required />

      <button type="submit">PRIJAVI SE</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      console.log("Login attempt:", this.email, this.password); // Provera da li funkcija radi

      try {
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          email: this.email,
          password: this.password,
        });

        if (response.data.status === "success") {
          // ovde cuvamo ID ulogovanog korisnika u localStorage pod kljucem "ulogovan_id"
          localStorage.setItem("ulogovan_id", response.data.ulogovan_id);

          this.$router.push({ name: response.data.redirect });
        } else {
          this.errorMessage = response.data.message || "Greška pri prijavi";
        }
      } catch (error) {
        console.error("Login error:", error.response?.data || error.message);
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "Došlo je do greške. Pokušajte ponovo.";
        }
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-form {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

input[type="email"],
input[type="password"],
button {
  width: 100%;
  padding: 12px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #d4af37;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

button:hover {
  background-color: #c68f28;
}

.flash-message {
  background-color: #ffffff;
  color: #d8000c;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 15px;
  text-align: center;
}

.fade-out {
  animation: fadeOut 1s ease-out forwards;
}

@keyframes fadeOut {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
