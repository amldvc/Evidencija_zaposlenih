<template>
  <div id="app">
    <Navbar v-if="!isLoginPage" /> 
    <router-view />
  </div>
</template>

<script>
import Navbar from "./components/navbar.vue";
import "@/assets/css/style.css";

export default {
  components: {
    Navbar,
  },
  computed: {
    isLoginPage() {
      return this.$route.path === "/";
    }
  }
};
</script>

<style>
/* Globalni stilovi */
</style>
