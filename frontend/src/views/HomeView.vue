<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavBar from '../components/NavBar.vue'

</script>

<template>
  <div class="home">
    <NavBar />
    <main class="main-content">
      <p>Jam Date Homepage</p>
    </main>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  margin-top: 10px;
  width: 100%;
}

.content-section {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}
</style>
