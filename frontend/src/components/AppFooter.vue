<template>
  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <strong>Vue E-Shop</strong>
        <p>Your one-stop shop for everything you need.</p>
      </div>
      <div class="footer-links">
        <RouterLink to="/products">Products</RouterLink>
        <RouterLink to="/cart">Cart</RouterLink>
        <RouterLink to="/orders">Orders</RouterLink>
      </div>
      <p class="footer-copy">&copy; 2026 Vue E-Shop. Built with Vue.js + FastAPI.</p>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.footer {
  background: var(--gray-900);
  color: var(--gray-400);
  padding: 3rem 0 1.5rem;
  margin-top: auto;
}

.footer-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
}

.footer-brand strong {
  color: white;
  font-size: 1.125rem;
}

.footer-brand p {
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.footer-links {
  display: flex;
  gap: 2rem;
}

.footer-links a {
  color: var(--gray-400);
  font-size: 0.875rem;
}

.footer-links a:hover { color: white; }

.footer-copy {
  font-size: 0.8125rem;
  border-top: 1px solid var(--gray-700);
  padding-top: 1.5rem;
  width: 100%;
}
</style>
