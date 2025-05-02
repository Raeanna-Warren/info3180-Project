import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/logout',
      name: 'logout',
      component: () => import('@/views/LogoutView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      // meta: { requiresAuth: true }
    },
    {
      path: '/profile/:profile_id',
      name: 'my-profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/new',
      name: 'profile-new',
      component: () => import('@/views/AddProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/profile/favourites',
      name: 'profile-favourites',
      component: () => import('@/views/ProfileFavouritesView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/users/:user_id',
      name: 'user-profile',
      component: () => import('@/views/UserProfileView.vue'),
      meta: { requiresAuth: true }
    },
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/home')
  } else {
    next()
  }
})

export default router
