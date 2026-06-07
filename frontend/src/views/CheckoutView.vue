<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { orderApi } from '../api'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const cart = useCartStore()

const form = ref({ shipping_address: '', phone: '' })
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  await cart.fetchCart()
  if (!cart.items.length) {
    router.push('/cart')
  }
})

async function placeOrder() {
  if (!form.value.shipping_address || !form.value.phone) {
    error.value = 'Please fill in all fields'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await orderApi.create(form.value)
    await cart.fetchCart()
    router.push('/orders')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to place order'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container">
    <h1 class="page-title">Checkout</h1>

    <div class="checkout-layout">
      <div class="checkout-form card">
        <h3>Shipping Information</h3>
        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <div class="form-group">
          <label>Shipping Address</label>
          <textarea
            v-model="form.shipping_address"
            class="form-input"
            rows="3"
            placeholder="Enter your full shipping address"
          />
        </div>
        <div class="form-group">
          <label>Phone Number</label>
          <input v-model="form.phone" type="tel" class="form-input" placeholder="Your phone number" />
        </div>
        <button class="btn btn-lg btn-primary" :disabled="loading" @click="placeOrder">
          {{ loading ? 'Placing Order...' : 'Place Order' }}
        </button>
      </div>

      <div class="order-summary card">
        <h3>Order Summary</h3>
        <div v-for="item in cart.items" :key="item.product_id" class="summary-item">
          <img :src="item.image" :alt="item.name" />
          <div>
            <p class="item-name">{{ item.name }}</p>
            <p class="item-qty">Qty: {{ item.quantity }}</p>
          </div>
          <span class="item-price">${{ item.subtotal.toFixed(2) }}</span>
        </div>
        <div class="summary-total">
          <span>Total</span>
          <span>${{ cart.total.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 2rem;
  align-items: start;
}

.checkout-form, .order-summary {
  padding: 1.5rem;
}

.checkout-form h3, .order-summary h3 {
  font-size: 1.125rem;
  margin-bottom: 1.25rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--gray-100);
}

.summary-item img {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: var(--radius);
}

.item-name {
  font-size: 0.875rem;
  font-weight: 500;
}

.item-qty {
  font-size: 0.8125rem;
  color: var(--gray-400);
}

.item-price {
  margin-left: auto;
  font-weight: 600;
  font-size: 0.875rem;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  margin-top: 0.5rem;
  border-top: 1px solid var(--gray-200);
  font-weight: 700;
  font-size: 1.125rem;
}

@media (max-width: 768px) {
  .checkout-layout { grid-template-columns: 1fr; }
}
</style>
