<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const auth = useAuthStore()
const cart = useCartStore()
</script>

<template>
  <header class="navbar">
    <div class="container navbar-inner">
      <RouterLink to="/" class="logo">
        <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
          <rect width="32" height="32" rx="8" fill="#6366f1"/>
          <path d="M8 10h16l-1.5 12H9.5L8 10z" stroke="white" stroke-width="1.5" fill="none"/>
          <circle cx="12" cy="26" r="2" fill="white"/>
          <circle cx="22" cy="26" r="2" fill="white"/>
        </svg>
        <span>Vue E-Shop</span>
      </RouterLink>

      <nav class="nav-links">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/products">Products</RouterLink>
        <RouterLink v-if="auth.isAdmin" to="/admin">Admin</RouterLink>
      </nav>

      <div class="nav-actions">
        <RouterLink v-if="auth.isLoggedIn" to="/cart" class="cart-link">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
            <path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/>
          </svg>
          <span v-if="cart.itemCount" class="cart-badge">{{ cart.itemCount }}</span>
        </RouterLink>

        <template v-if="auth.isLoggedIn">
          <RouterLink to="/orders" class="btn btn-sm btn-outline">Orders</RouterLink>
          <span class="user-name">{{ auth.user?.name }}</span>
          <button class="btn btn-sm btn-outline" @click="auth.logout(); cart.clearCart()">Logout</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn btn-sm btn-outline">Login</RouterLink>
          <RouterLink to="/register" class="btn btn-sm btn-primary">Sign Up</RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  background: white;
  border-bottom: 1px solid var(--gray-200);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--gray-900);
}

.logo:hover { color: var(--primary); }

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  color: var(--gray-600);
  font-weight: 500;
  font-size: 0.9375rem;
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cart-link {
  position: relative;
  color: var(--gray-600);
  padding: 0.375rem;
}

.cart-link:hover { color: var(--primary); }

.cart-badge {
  position: absolute;
  top: -4px;
  right: -8px;
  background: var(--primary);
  color: white;
  font-size: 0.6875rem;
  font-weight: 600;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 0.875rem;
  color: var(--gray-600);
  font-weight: 500;
}

@media (max-width: 768px) {
  .nav-links { display: none; }
  .user-name { display: none; }
}
</style>
