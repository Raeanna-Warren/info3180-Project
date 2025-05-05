import { defineStore } from 'pinia'
import axios from 'axios'
import api from '@/services/ApiService'

const API_URL = 'http://localhost:5000/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: localStorage.getItem('user') || ""
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user
  },

  actions: {
    async login(username, password) {
      try {
        const response = await axios.post(`${API_URL}/auth/login`, {
          username,
          password
        })
        
        const { access_token, user } = response.data
        this.token = access_token
        this.user = user
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify(user))
        
        // Set default authorization header for all future requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        api.setAuthToken(access_token)
        
        return response.data
      } catch (error) {
        throw error
      }
    },

    async register(username, name, email, password) {
      try {
        const response = await axios.post(`${API_URL}/auth/register`, {
          username,
          name,
          email,
          password
        })
        return response.data
      } catch (error) {
        throw error
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },

    // Initialize auth state from localStorage
    initializeAuth() {
      const token = localStorage.getItem('token')
      const rawUser = localStorage.getItem('user')
      const user = rawUser ? rawUser : null
      
      if (token && user) {
        this.token = token
        this.user = user
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    }
  }
}) 