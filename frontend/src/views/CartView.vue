<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const cart = useCartStore()
const updating = ref(null)

onMounted(() => cart.fetchCart())

async function updateQuantity(productId, quantity) {
  updating.value = productId
  try {
    if (quantity < 1) {
      await cart.removeItem(productId)
    } else {
      await cart.updateItem(productId, quantity)
    }
  } finally {
    updating.value = null
  }
}

async function removeItem(productId) {
  await cart.removeItem(productId)
}
</script>

<template>
  <div class="container">
    <h1 class="page-title">Shopping Cart</h1>

    <div v-if="cart.loading" class="loading">Loading cart...</div>

    <div v-else-if="!cart.items.length" class="empty-state">
      <h3>Your cart is empty</h3>
      <p>Add some products to get started!</p>
      <RouterLink to="/products" class="btn btn-primary" style="margin-top: 1rem">Browse Products</RouterLink>
    </div>

    <div v-else class="cart-layout">
      <div class="cart-items">
        <div v-for="item in cart.items" :key="item.product_id" class="cart-item card">
          <img :src="item.image" :alt="item.name" class="item-image" />
          <div class="item-details">
            <h3>{{ item.name }}</h3>
            <p class="item-price">${{ item.price.toFixed(2) }}</p>
          </div>
          <div class="quantity-control">
            <button
              :disabled="updating === item.product_id"
              @click="updateQuantity(item.product_id, item.quantity - 1)"
            >-</button>
            <span>{{ item.quantity }}</span>
            <button
              :disabled="updating === item.product_id"
              @click="updateQuantity(item.product_id, item.quantity + 1)"
            >+</button>
          </div>
          <div class="item-subtotal">${{ item.subtotal.toFixed(2) }}</div>
          <button class="remove-btn" @click="removeItem(item.product_id)" title="Remove">
            &times;
          </button>
        </div>
      </div>

      <div class="cart-summary card">
        <h3>Order Summary</h3>
        <div class="summary-row">
          <span>Items ({{ cart.itemCount }})</span>
          <span>${{ cart.total.toFixed(2) }}</span>
        </div>
        <div class="summary-row total">
          <span>Total</span>
          <span>${{ cart.total.toFixed(2) }}</span>
        </div>
        <button class="btn btn-lg btn-primary checkout-btn" @click="router.push('/checkout')">
          Proceed to Checkout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
export default { components: { RouterLink } }
</script>

<style scoped>
.cart-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 2rem;
  align-items: start;
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  margin-bottom: 1rem;
}

.item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius);
}

.item-details h3 {
  font-size: 0.9375rem;
  font-weight: 600;
}

.item-price {
  color: var(--gray-500);
  font-size: 0.875rem;
}

.quantity-control {
  display: flex;
  align-items: center;
  border: 1px solid var(--gray-300);
  border-radius: var(--radius);
}

.quantity-control button {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--gray-50);
  font-size: 1rem;
}

.quantity-control span {
  width: 36px;
  text-align: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.item-subtotal {
  font-weight: 700;
  font-size: 1rem;
  min-width: 70px;
  text-align: right;
}

.remove-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--gray-400);
  padding: 0.25rem;
}

.remove-btn:hover { color: var(--danger); }

.cart-summary {
  padding: 1.5rem;
  position: sticky;
  top: 80px;
}

.cart-summary h3 {
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  font-size: 0.9375rem;
  color: var(--gray-600);
}

.summary-row.total {
  border-top: 1px solid var(--gray-200);
  margin-top: 0.5rem;
  padding-top: 1rem;
  font-weight: 700;
  font-size: 1.125rem;
  color: var(--gray-900);
}

.checkout-btn {
  width: 100%;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .cart-layout { grid-template-columns: 1fr; }
  .cart-item {
    grid-template-columns: 60px 1fr;
    grid-template-rows: auto auto;
  }
  .item-image { width: 60px; height: 60px; }
}
</style>
