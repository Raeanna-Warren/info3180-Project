<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
    <nav class="navbar">
      <div class="nav-brand">Jam Date</div>
      <div class="nav-links">
        <router-link to="/home" class="nav-link">Home</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/profile" class="nav-link">Profile</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/profile/new" class="nav-link">Add Profile</router-link>
        <router-link to="/view-reports" class="nav-link">View Reports</router-link>

        <router-link v-if="!authStore.isAuthenticated" to="/register" class="nav-link">Register</router-link>
        <router-link v-if="!authStore.isAuthenticated" to="/login" class="nav-link">Login</router-link>
        <button v-if="authStore.isAuthenticated" @click="authStore.logout" class="nav-link logout-btn">Logout</button>
      </div>
    </nav>
</template>

<style scoped>
.navbar {
  background-color: #4CAF50;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}
</style>