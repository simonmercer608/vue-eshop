<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi, categoryApi } from '../api'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'
import ProductCard from '../components/ProductCard.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

const products = ref([])
const categories = ref([])
const loading = ref(true)
const search = ref(route.query.search || '')
const selectedCategory = ref(route.query.category || '')
const message = ref('')

async function loadProducts() {
  loading.value = true
  try {
    const params = { limit: 50 }
    if (search.value) params.search = search.value
    if (selectedCategory.value) params.category = selectedCategory.value
    const { data } = await productApi.list(params)
    products.value = data
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const { data } = await categoryApi.list()
  categories.value = data
  await loadProducts()
})

watch([search, selectedCategory], () => {
  router.replace({
    query: {
      ...(search.value && { search: search.value }),
      ...(selectedCategory.value && { category: selectedCategory.value }),
    },
  })
  loadProducts()
})

async function handleAddToCart(product) {
  if (!auth.isLoggedIn) {
    router.push({ name: 'login', query: { redirect: '/products' } })
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
  <div class="container">
    <h1 class="page-title">Products</h1>
    <p class="page-subtitle">Browse our full catalog of products</p>

    <div class="filters">
      <input
        v-model="search"
        type="text"
        class="form-input search-input"
        placeholder="Search products..."
      />
      <select v-model="selectedCategory" class="form-input category-select">
        <option value="">All Categories</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
    </div>

    <div v-if="message" class="alert alert-success">{{ message }}</div>

    <div v-if="loading" class="loading">Loading products...</div>

    <div v-else-if="products.length" class="grid grid-4">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        @add-to-cart="handleAddToCart"
      />
    </div>

    <div v-else class="empty-state">
      <h3>No products found</h3>
      <p>Try adjusting your search or filters.</p>
    </div>
  </div>
</template>

<style scoped>
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input {
  flex: 1;
}

.category-select {
  width: 200px;
}

@media (max-width: 768px) {
  .filters { flex-direction: column; }
  .category-select { width: 100%; }
}
</style>
