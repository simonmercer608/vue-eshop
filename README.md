# Vue E-Shop
# 114 Team deveolpers

A full-stack ecommerce website built with **Vue.js**, **FastAPI**, **MongoDB**, and **Redis**.

## Features

- Product catalog with search and category filtering
- Featured products on homepage
- User registration and JWT authentication
- Shopping cart stored in Redis
- Order placement with stock management
- Admin panel for product CRUD (first registered user becomes admin)
- Responsive modern UI

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | Vue 3, Vite, Pinia, Vue Router      |
| Backend  | FastAPI, Motor (async MongoDB)      |
| Database | MongoDB                             |
| Cache    | Redis (product cache + shopping cart) |

## Project Structure

```
vue-eshop/
├── backend/          # FastAPI REST API
│   ├── app/
│   │   ├── routers/  # API route handlers
│   │   ├── main.py   # App entry point
│   │   └── ...
│   ├── seed.py       # Database seeder
│   └── requirements.txt
├── frontend/         # Vue.js SPA
│   ├── src/
│   │   ├── views/    # Page components
│   │   ├── components/
│   │   ├── stores/   # Pinia state management
│   │   └── api/      # Axios API client
│   └── package.json
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for MongoDB and Redis)

### 1. Start MongoDB and Redis

```bash
docker compose up -d
```

### 2. Set up the Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python seed.py
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Set up the Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## Usage

1. Open http://localhost:5173
2. Register an account (first user becomes admin)
3. Browse products, add to cart, and checkout
4. Admin users can manage products at `/admin`

## API Endpoints

| Method | Endpoint                  | Description          |
|--------|---------------------------|----------------------|
| POST   | `/api/auth/register`      | Register user        |
| POST   | `/api/auth/login`         | Login                |
| GET    | `/api/auth/me`            | Current user         |
| GET    | `/api/products`           | List products        |
| GET    | `/api/products/{id}`      | Product detail       |
| POST   | `/api/products`           | Create product (admin) |
| GET    | `/api/categories`         | List categories      |
| GET    | `/api/cart`               | Get cart             |
| POST   | `/api/cart/items`         | Add to cart          |
| POST   | `/api/orders`             | Place order          |
| GET    | `/api/orders`             | List orders          |

## License

MIT
