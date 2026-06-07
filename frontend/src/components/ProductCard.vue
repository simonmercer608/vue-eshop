<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  product: { type: Object, required: true },
})

const emit = defineEmits(['add-to-cart'])

function formatPrice(price) {
  return `$${price.toFixed(2)}`
}
</script>

<template>
  <div class="product-card card">
    <RouterLink :to="`/products/${product.id}`" class="product-image">
      <img :src="product.image" :alt="product.name" loading="lazy" />
      <span v-if="product.featured" class="featured-badge">Featured</span>
    </RouterLink>
    <div class="product-info">
      <span v-if="product.category_name" class="category">{{ product.category_name }}</span>
      <RouterLink :to="`/products/${product.id}`" class="product-name">
        {{ product.name }}
      </RouterLink>
      <div class="product-footer">
        <span class="price">{{ formatPrice(product.price) }}</span>
        <button class="btn btn-sm btn-primary" @click.prevent="emit('add-to-cart', product)">
          Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-image {
  position: relative;
  display: block;
  aspect-ratio: 1;
  overflow: hidden;
  background: var(--gray-100);
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.featured-badge {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  background: var(--primary);
  color: white;
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.product-info {
  padding: 1rem;
}

.category {
  font-size: 0.75rem;
  color: var(--gray-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.product-name {
  display: block;
  font-weight: 600;
  color: var(--gray-800);
  margin: 0.25rem 0 0.75rem;
  font-size: 0.9375rem;
  line-height: 1.4;
}

.product-name:hover { color: var(--primary); }

.product-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.price {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--primary);
}
</style>
