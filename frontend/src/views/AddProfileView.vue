<script setup>
import NavBar from '@/components/NavBar.vue'
import { ref } from 'vue'
import api from '@/services/ApiService'

const description = ref('')
const parish = ref('')
const biography = ref('')
const sex = ref('')
const race = ref('')
const birth_year = ref('')
const height = ref('')
const fav_cuisine = ref('')
const fav_colour = ref('')
const fav_school_subject = ref('')
const political = ref(null)
const religious = ref(null)
const family_oriented = ref(null)

async function handleSubmit() {
  const profileData = {
    description: description.value,
    parish: parish.value,
    biography: biography.value,
    sex: sex.value,
    race: race.value,
    birth_year: parseInt(birth_year.value),
    height: parseFloat(height.value),
    fav_cuisine: fav_cuisine.value,
    fav_colour: fav_colour.value,
    fav_school_subject: fav_school_subject.value,
    political: political.value === 'true',
    religious: religious.value === 'true',
    family_oriented: family_oriented.value === 'true'
  }

    try {
        const response = await api.post("/profiles", profileData)
    console.log(response)
    }
    catch (err) {
    console.log(err)
  }

  console.log('Submitting profile:', profileData)
  // TODO: send data to backend
}
</script>

<template>
  <div class="content">
    <NavBar />

    <main class="main-content">
      <p class="heading">Add Profile</p>
      <div class="profile-section">
        <form @submit.prevent="handleSubmit" class="profile-form">
          <div class="form-group"><label>Description:</label><input class="form-control" v-model="description" required /></div>
          <div class="form-group"><label>Parish:</label><input class="form-control" v-model="parish" required /></div>
          <div class="form-group"><label>Biography:</label><textarea class="form-control" v-model="biography" required /></div>
          <div class="form-group"><label>Sex:</label><input class="form-control" v-model="sex" required /></div>
          <div class="form-group"><label>Race:</label><input class="form-control" v-model="race" required /></div>
          <div class="form-group"><label>Birth Year:</label><input class="form-control" type="number" v-model="birth_year" required /></div>
          <div class="form-group"><label>Height (m):</label><input class="form-control" type="number" step="0.01" v-model="height" required /></div>
          <div class="form-group"><label>Favorite Cuisine:</label><input class="form-control" v-model="fav_cuisine" required /></div>
          <div class="form-group"><label>Favorite Colour:</label><input class="form-control" v-model="fav_colour" required /></div>
          <div class="form-group"><label>Favorite School Subject:</label><input class="form-control" v-model="fav_school_subject" required /></div>

          <div class="form-group">
            <label>Political:</label>
            <select v-model="political" required>
              <option disabled value="">Select</option>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>

          <div class="form-group">
            <label>Religious:</label>
            <select v-model="religious" required>
              <option disabled value="">Select</option>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>

          <div class="form-group">
            <label>Family Oriented:</label>
            <select v-model="family_oriented" required>
              <option disabled value="">Select</option>
              <option value="true">Yes</option>
              <option value="false">No</option>
            </select>
          </div>

          <button type="submit" class="btn-primary">Submit</button>
        </form>
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

.main-content {
  padding: 2rem;
}

.heading {
  font-size: 32px;
  margin-bottom: 1rem;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
}

/* .form-group {
  display: flex;
  flex-direction: column;
} */

/* .form-group label {
  font-weight: bold;
  margin-bottom: 0.25rem;
} */

/* .form-group input,
.form-group textarea, */
.form-group select {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* .btn-primary {
  padding: 0.75rem 1.5rem;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
} */
</style>
