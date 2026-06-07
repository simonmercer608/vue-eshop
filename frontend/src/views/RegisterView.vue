<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const form = ref({ name: '', email: '', password: '' })

async function handleRegister() {
  const ok = await auth.register(form.value)
  if (ok) {
    router.push('/')
  }
}
</script>

<template>
  <div class="container auth-page">
    <div class="auth-card card">
      <h1 class="page-title">Create Account</h1>
      <p class="page-subtitle">Join Vue E-Shop today</p>

      <div v-if="auth.error" class="alert alert-error">{{ auth.error }}</div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Full Name</label>
          <input v-model="form.name" type="text" class="form-input" required placeholder="John Doe" />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input v-model="form.email" type="email" class="form-input" required placeholder="you@example.com" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="form.password" type="password" class="form-input" required minlength="6" placeholder="Min 6 characters" />
        </div>
        <button type="submit" class="btn btn-lg btn-primary auth-btn" :disabled="auth.loading">
          {{ auth.loading ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="auth-link">
        Already have an account? <RouterLink to="/login">Sign in</RouterLink>
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
