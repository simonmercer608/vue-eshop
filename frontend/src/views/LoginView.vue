<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

const email = ref('')
const password = ref('')

async function handleLogin() {
  const ok = await auth.login(email.value, password.value)
  if (ok) {
    await cart.fetchCart()
    router.push(route.query.redirect || '/')
  }
}
</script>

<template>
  <div class="container auth-page">
    <div class="auth-card card">
      <h1 class="page-title">Welcome Back</h1>
      <p class="page-subtitle">Sign in to your account</p>

      <div v-if="auth.error" class="alert alert-error">{{ auth.error }}</div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input v-model="email" type="email" class="form-input" required placeholder="you@example.com" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" class="form-input" required placeholder="Your password" />
        </div>
        <button type="submit" class="btn btn-lg btn-primary auth-btn" :disabled="auth.loading">
          {{ auth.loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="auth-link">
        Don't have an account? <RouterLink to="/register">Sign up</RouterLink>
      </p>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
export default { components: { RouterLink } }
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
}

.auth-btn {
  width: 100%;
  margin-top: 0.5rem;
}

.auth-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.875rem;
  color: var(--gray-500);
}
</style>
