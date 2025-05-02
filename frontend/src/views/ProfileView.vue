<template>
  <div class="content">
    <NavBar />

    <main class="main-content">
      <h1>Profile</h1>
      <div class="profile-section">
        <div class="profile-info">
          <h2>User Information</h2>
          <div class="info-group">
            <label>Username:</label>
            <p>{{ user?.username }}</p>
          </div>
          <div class="info-group">
            <label>Email:</label>
            <p>{{ user?.email }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.getUser)

</script>

<style scoped>
.content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

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

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.profile-section {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.profile-info {
  max-width: 600px;
}

.info-group {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.info-group label {
  font-weight: bold;
  color: #666;
  display: block;
  margin-bottom: 0.5rem;
}

.info-group p {
  margin: 0;
  color: #333;
}
</style> 