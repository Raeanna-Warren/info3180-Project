<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'
import api from '@/services/ApiService'
import { Star } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const user = computed(() => authStore.getUser)

const defaultPhoto = '/default_image.jpg'

const profiles = ref([])
const search = ref({
  name: '',
  birthYear: '',
  sex: '',
  race: ''
})

const favorites = ref([])

function isFavorite(profileId) {
  return favorites.value.includes(profileId)
}

async function toggleFavorite(userId) {
  try {
    await api.post(`/profiles/${userId}/favourite`)
  } catch (error) {
    console.error('Failed to favorite:', error)
  }
}


function viewProfile(profileId) {
  console.log(profileId)
  router.push({ name: 'profile-details', params: { id: profileId } })
}

async function applyFilters() {
  try {
    const response = await api.get('/search/', {
      params: {
        name: search.value.name,
        birth_year: search.value.birthYear,
        sex: search.value.sex,
        race: search.value.race
      }
    })

    profiles.value = response.data
  } catch (error) {
    console.error("Error fetching filtered profiles", error)
  }
}

function resetFilters() {
  search.value = {
    name: '',
    birthYear: '',
    sex: '',
    race: ''
  }
  fetchProfiles()
}

async function fetchProfiles() {
  try {
    const response = await api.get('/profiles/')
    profiles.value = response.data
    console.log(response)
  } catch (err) {
    alert("Please create a profile first!")
    console.log(err)
  }
}

onMounted(() => {
  fetchProfiles()
})
</script>

<template>
  <div class="content">
    <NavBar />

    <main class="main-content">
      <div class="header-section">
        <p class="heading">Profiles</p>
      </div>

      <div class="search-section">
        <input v-model="search.name" type="text" placeholder="Search by name" />
        <input v-model="search.birthYear" type="text" placeholder="Birth year" />
        <select v-model="search.sex">
          <option disabled value="">Sex</option>
          <option>Male</option>
          <option>Female</option>
        </select>
        <input v-model="search.race" type="text" placeholder="Race" />
        <button @click="applyFilters">Filter</button>
      <button @click="resetFilters">Reset</button>
      </div>
      <div class="profiles-section">
        <div class="profile" v-for="profile in profiles" v-bind:key="profile.id" @click="viewProfile(profile.id)">
          <div class="profile-card">
            <button
        v-if="profile.user.id !== user.user_id"
        class="favorite-btn"
        @click.stop="toggleFavorite(profile.user.id)"
      >
        <Star
          :color="profile.is_favorited ? '#facc15' : '#a1a1aa'"
          :fill="profile.is_favorited ? '#facc15' : 'none'"
          class="w-6 h-6"
        />
      </button>
            <div class="profile-header">
              <img
                :src="profile.user.photo || defaultPhoto"
                alt="Profile Picture"
                class="profile-image"
              />
              <div class="profile-info">
                <h2 class="name">{{ profile.user.name }}</h2>
                <p class="parish">{{ profile.parish }}</p>
              </div>
            </div>
            <p class="description">{{ profile.description }}</p>
            <p class="bio">{{ profile.biography }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.content {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.profiles-section {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 5px;
}

.profile-card {
  position: relative;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  max-width: 400px;
  width: 400px;
  transition: transform 0.2s ease;
}
.profile-card:hover {
  transform: translateY(-4px);
}
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 9999px;
  object-fit: cover;
  margin-right: 1rem;
  border: 2px solid #ddd;
}
.profile-info .name {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}
.profile-info .parish {
  color: #6b7280;
  font-size: 0.875rem;
}
.description {
  font-size: 0.95rem;
  color: #374151;
  margin-bottom: 0.5rem;
}
.bio {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.4;
}

.main-content {
  padding: 2rem;
}

.search-section {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.search-section input,
.search-section select {
  padding: 0.5rem 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  width: 180px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.favorite-btn {
  z-index: 999;
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  cursor: pointer;
}

.heading {
  font-size: 1.8rem;
  font-weight: 600;
}

.search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  width: 220px;
}

.search-section button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
}

.search-section button:last-of-type {
  background-color: #e74c3c;
}
</style>
