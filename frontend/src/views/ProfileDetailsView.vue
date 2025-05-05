<template>
  <div class="content">
    <NavBar />

    <main class="main-content">
      <div class="profile-details">
        <div v-if="profile">
          <h1>{{ profile.user.username }}</h1>
          <img
            :src="profile.user.photo || defaultPhoto"
            alt="Profile Picture"
            class="profile-image"
          />
          <p><strong>Parish:</strong> {{ profile.parish }}</p>
          <p><strong>Biography:</strong> {{ profile.biography }}</p>
          <p><strong>Sex:</strong> {{ profile.sex }}</p>
          <p><strong>Race:</strong> {{ profile.race }}</p>
          <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
          <p><strong>Height:</strong> {{ profile.height }}</p>
          <p><strong>Favorite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
          <p><strong>Favorite Color:</strong> {{ profile.fav_colour }}</p>
          <p><strong>Favorite School Subject:</strong> {{ profile.fav_school_subject }}</p>
        </div>
        <div v-else>
          <p>Loading profile...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

import api from '@/services/ApiService'

const route = useRoute()
const profile = ref(null)
const defaultPhoto = '/default_image.jpg'

onMounted(async () => {
  const profileId = route.params.id
  try {
    const response = await api.get(`/profiles/${profileId}`)
    profile.value = response.data
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
})
</script>

<style scoped>
.profile-details {
  padding: 20px;
}

.profile-image {
  max-width: 200px;
  height: auto;
  border-radius: 50%;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
}

p {
  font-size: 1rem;
  line-height: 1.6;
}

strong {
  font-weight: bold;
}
</style>
