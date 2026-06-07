<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { productApi } from '../api'
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const cart = useCartStore()

const product = ref(null)
const loading = ref(true)
const quantity = ref(1)
const message = ref('')
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await productApi.get(route.params.id)
    product.value = data
  } catch {
    error.value = 'Product not found'
  } finally {
    loading.value = false
  }
})

async function addToCart() {
  if (!auth.isLoggedIn) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  try {
    await cart.addItem(product.value.id, quantity.value)
    message.value = 'Added to cart!'
    setTimeout(() => { message.value = '' }, 3000)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to add to cart'
  }
}
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="error && !product" class="empty-state">
      <h3>{{ error }}</h3>
      <RouterLink to="/products" class="btn btn-primary" style="margin-top: 1rem">Back to Products</RouterLink>
    </div>

    <div v-else-if="product" class="product-detail">
      <div class="product-gallery">
        <img :src="product.image" :alt="product.name" />
      </div>
      <div class="product-content">
        <span v-if="product.category_name" class="category">{{ product.category_name }}</span>
        <h1 class="page-title">{{ product.name }}</h1>
        <p class="price">${{ product.price.toFixed(2) }}</p>
        <p class="description">{{ product.description }}</p>

        <div class="stock-info">
          <span :class="product.stock > 0 ? 'in-stock' : 'out-of-stock'">
            {{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}
          </span>
        </div>

        <div v-if="message" class="alert alert-success">{{ message }}</div>
        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <div class="actions">
          <div class="quantity-control">
            <button @click="quantity = Math.max(1, quantity - 1)" :disabled="quantity <= 1">-</button>
            <span>{{ quantity }}</span>
            <button @click="quantity = Math.min(product.stock, quantity + 1)" :disabled="quantity >= product.stock">+</button>
          </div>
          <button
            class="btn btn-lg btn-primary"
            :disabled="product.stock === 0"
            @click="addToCart"
          >
            Add to Cart
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-detail {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: start;
}

.product-gallery {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.product-gallery img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.category {
  font-size: 0.8125rem;
  color: var(--gray-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.price {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary);
  margin: 0.5rem 0 1rem;
}

.description {
  color: var(--gray-600);
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.stock-info { margin-bottom: 1.5rem; }

.in-stock { color: var(--success); font-weight: 500; }
.out-of-stock { color: var(--danger); font-weight: 500; }

.actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.quantity-control {
  display: flex;
  align-items: center;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius);
  overflow: hidden;
}

.quantity-control button {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--gray-50);
  font-size: 1.125rem;
  color: var(--gray-700);
}

.quantity-control button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.quantity-control span {
  width: 48px;
  text-align: center;
  font-weight: 600;
}

@media (max-width: 768px) {
  .product-detail { grid-template-columns: 1fr; gap: 1.5rem; }
}
</style>
