<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '../api'

const orders = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await orderApi.list()
    orders.value = data
  } finally {
    loading.value = false
  }
})

function statusClass(status) {
  const map = { pending: 'badge-warning', shipped: 'badge-info', delivered: 'badge-success' }
  return map[status] || 'badge-info'
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  })
}
</script>

<template>
  <div class="container">
    <h1 class="page-title">My Orders</h1>
    <p class="page-subtitle">Track your order history</p>

    <div v-if="loading" class="loading">Loading orders...</div>

    <div v-else-if="!orders.length" class="empty-state">
      <h3>No orders yet</h3>
      <p>Start shopping to see your orders here!</p>
      <RouterLink to="/products" class="btn btn-primary" style="margin-top: 1rem">Browse Products</RouterLink>
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card card">
        <div class="order-header">
          <div>
            <span class="order-id">Order #{{ order.id.slice(-8) }}</span>
            <span class="order-date">{{ formatDate(order.created_at) }}</span>
          </div>
          <span :class="['badge', statusClass(order.status)]">{{ order.status }}</span>
        </div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.product_id" class="order-item">
            <span>{{ item.name }} x {{ item.quantity }}</span>
            <span>${{ item.subtotal.toFixed(2) }}</span>
          </div>
        </div>
        <div class="order-footer">
          <span>Ship to: {{ order.shipping_address }}</span>
          <span class="order-total">Total: ${{ order.total.toFixed(2) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
export default { components: { RouterLink } }
</script>

<style scoped>
.order-card {
  padding: 1.5rem;
  margin-bottom: 1rem;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--gray-100);
}

.order-id {
  font-weight: 600;
  font-size: 0.9375rem;
}

.order-date {
  display: block;
  font-size: 0.8125rem;
  color: var(--gray-400);
  margin-top: 0.125rem;
}

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 0.375rem 0;
  font-size: 0.875rem;
  color: var(--gray-600);
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--gray-100);
  font-size: 0.8125rem;
  color: var(--gray-500);
}

.order-total {
  font-weight: 700;
  font-size: 1rem;
  color: var(--gray-900);
}
</style>
