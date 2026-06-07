import { defineStore } from 'pinia'
import { ref } from 'vue'
import { cartApi } from '../api'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const total = ref(0)
  const itemCount = ref(0)
  const loading = ref(false)

  async function fetchCart() {
    loading.value = true
    try {
      const { data } = await cartApi.get()
      items.value = data.items
      total.value = data.total
      itemCount.value = data.item_count
    } catch {
      items.value = []
      total.value = 0
      itemCount.value = 0
    } finally {
      loading.value = false
    }
  }

  async function addItem(productId, quantity = 1) {
    const { data } = await cartApi.addItem(productId, quantity)
    items.value = data.items
    total.value = data.total
    itemCount.value = data.item_count
  }

  async function updateItem(productId, quantity) {
    const { data } = await cartApi.updateItem(productId, quantity)
    items.value = data.items
    total.value = data.total
    itemCount.value = data.item_count
  }

  async function removeItem(productId) {
    const { data } = await cartApi.removeItem(productId)
    items.value = data.items
    total.value = data.total
    itemCount.value = data.item_count
  }

  async function clearCart() {
    await cartApi.clear()
    items.value = []
    total.value = 0
    itemCount.value = 0
  }

  return { items, total, itemCount, loading, fetchCart, addItem, updateItem, removeItem, clearCart }
})
