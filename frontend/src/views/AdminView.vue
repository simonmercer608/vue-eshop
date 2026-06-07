<script setup>
import { ref, onMounted } from 'vue'
import { productApi, categoryApi } from '../api'

const products = ref([])
const categories = ref([])
const loading = ref(true)
const showForm = ref(false)
const editingId = ref(null)
const error = ref('')
const success = ref('')

const emptyForm = () => ({
  name: '', description: '', price: '', image: '', category_id: '', stock: '', featured: false,
})
const form = ref(emptyForm())

onMounted(async () => {
  await loadData()
})

async function loadData() {
  loading.value = true
  try {
    const [prodRes, catRes] = await Promise.all([
      productApi.list({ limit: 100 }),
      categoryApi.list(),
    ])
    products.value = prodRes.data
    categories.value = catRes.data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = emptyForm()
  showForm.value = true
}

function openEdit(product) {
  editingId.value = product.id
  form.value = {
    name: product.name,
    description: product.description,
    price: product.price,
    image: product.image,
    category_id: product.category_id,
    stock: product.stock,
    featured: product.featured,
  }
  showForm.value = true
}

async function saveProduct() {
  error.value = ''
  success.value = ''
  const payload = {
    ...form.value,
    price: parseFloat(form.value.price),
    stock: parseInt(form.value.stock),
  }
  try {
    if (editingId.value) {
      await productApi.update(editingId.value, payload)
      success.value = 'Product updated!'
    } else {
      await productApi.create(payload)
      success.value = 'Product created!'
    }
    showForm.value = false
    await loadData()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to save product'
  }
}

async function deleteProduct(id) {
  if (!confirm('Delete this product?')) return
  try {
    await productApi.delete(id)
    success.value = 'Product deleted!'
    await loadData()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to delete product'
  }
}
</script>

<template>
  <div class="container">
    <div class="admin-header">
      <div>
        <h1 class="page-title">Admin Panel</h1>
        <p class="page-subtitle">Manage your product catalog</p>
      </div>
      <button class="btn btn-primary" @click="openCreate">Add Product</button>
    </div>

    <div v-if="error" class="alert alert-error">{{ error }}</div>
    <div v-if="success" class="alert alert-success">{{ success }}</div>

    <div v-if="showForm" class="product-form card">
      <h3>{{ editingId ? 'Edit Product' : 'New Product' }}</h3>
      <div class="form-grid">
        <div class="form-group">
          <label>Name</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label>Price</label>
          <input v-model="form.price" type="number" step="0.01" class="form-input" required />
        </div>
        <div class="form-group">
          <label>Category</label>
          <select v-model="form.category_id" class="form-input" required>
            <option value="">Select category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Stock</label>
          <input v-model="form.stock" type="number" class="form-input" required />
        </div>
        <div class="form-group full-width">
          <label>Image URL</label>
          <input v-model="form.image" class="form-input" placeholder="https://..." />
        </div>
        <div class="form-group full-width">
          <label>Description</label>
          <textarea v-model="form.description" class="form-input" rows="3" required />
        </div>
        <div class="form-group">
          <label class="checkbox-label">
            <input v-model="form.featured" type="checkbox" /> Featured product
          </label>
        </div>
      </div>
      <div class="form-actions">
        <button class="btn btn-outline" @click="showForm = false">Cancel</button>
        <button class="btn btn-primary" @click="saveProduct">Save Product</button>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else class="admin-table card">
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Featured</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>
              <div class="product-cell">
                <img :src="product.image" :alt="product.name" />
                <span>{{ product.name }}</span>
              </div>
            </td>
            <td>{{ product.category_name }}</td>
            <td>${{ product.price.toFixed(2) }}</td>
            <td>{{ product.stock }}</td>
            <td>{{ product.featured ? 'Yes' : 'No' }}</td>
            <td>
              <button class="btn btn-sm btn-outline" @click="openEdit(product)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteProduct(product.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.product-form {
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.product-form h3 {
  margin-bottom: 1rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 1rem;
}

.form-group.full-width { grid-column: 1 / -1; }

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 400;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.admin-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.875rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  border-bottom: 1px solid var(--gray-100);
}

th {
  background: var(--gray-50);
  font-weight: 600;
  color: var(--gray-600);
}

.product-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.product-cell img {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: var(--radius);
}

td .btn { margin-right: 0.375rem; }

@media (max-width: 768px) {
  .form-grid { grid-template-columns: 1fr; }
  .admin-header { flex-direction: column; gap: 1rem; }
}
</style>
