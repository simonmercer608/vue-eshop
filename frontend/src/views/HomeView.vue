<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { productApi } from '../api'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'
import ProductCard from '../components/ProductCard.vue'

const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()
const featured = ref([])
const loading = ref(true)
const message = ref('')

onMounted(async () => {
  try {
    const { data } = await productApi.list({ featured: true, limit: 8 })
    featured.value = data
  } finally {
    loading.value = false
  }
})

async function handleAddToCart(product) {
  if (!auth.isLoggedIn) {
    router.push({ name: 'login', query: { redirect: `/products/${product.id}` } })
    return
  }
  try {
    await cart.addItem(product.id)
    message.value = `${product.name} added to cart!`
    setTimeout(() => { message.value = '' }, 3000)
  } catch (e) {
    message.value = e.response?.data?.detail || 'Failed to add to cart'
  }
}
</script>

<template>
  <div>
    <section class="hero">
      <div class="container hero-content">
        <h1>Discover Amazing Products</h1>
        <p>Shop the latest trends with fast delivery and great prices.</p>
        <RouterLink to="/products" class="btn btn-lg btn-primary">Browse Products</RouterLink>
      </div>
    </section>

    <section class="container">
      <div v-if="message" class="alert alert-success">{{ message }}</div>

      <h2 class="section-title">Featured Products</h2>

      <div v-if="loading" class="loading">Loading products...</div>

      <div v-else-if="featured.length" class="grid grid-4">
        <ProductCard
          v-for="product in featured"
          :key="product.id"
          :product="product"
          @add-to-cart="handleAddToCart"
        />
      </div>

      <div v-else class="empty-state">
        <h3>No featured products yet</h3>
        <p>Check back soon for new arrivals!</p>
      </div>

      <div class="view-all">
        <RouterLink to="/products" class="btn btn-outline btn-lg">View All Products</RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a78bfa 100%);
  color: white;
  padding: 5rem 0;
  margin-bottom: 3rem;
  text-align: center;
}

.hero h1 {
  font-size: 2.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.hero p {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.hero .btn-primary {
  background: white;
  color: var(--primary);
}

.hero .btn-primary:hover {
  background: var(--gray-100);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: var(--gray-900);
}

.view-all {
  text-align: center;
  margin-top: 2.5rem;
  padding-bottom: 1rem;
}

@media (max-width: 768px) {
  .hero h1 { font-size: 2rem; }
  .hero { padding: 3rem 0; }
}
</style>
