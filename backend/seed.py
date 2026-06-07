"""Seed the database with sample categories and products."""

import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

CATEGORIES = [
    {"name": "Electronics", "slug": "electronics"},
    {"name": "Clothing", "slug": "clothing"},
    {"name": "Home & Garden", "slug": "home-garden"},
    {"name": "Sports", "slug": "sports"},
    {"name": "Books", "slug": "books"},
]

PRODUCTS = [
    {
        "name": "Wireless Bluetooth Headphones",
        "description": "Premium noise-cancelling headphones with 30-hour battery life and crystal-clear sound quality.",
        "price": 79.99,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "category_slug": "electronics",
        "stock": 50,
        "featured": True,
    },
    {
        "name": "Smart Watch Pro",
        "description": "Track your fitness, receive notifications, and stay connected with this sleek smartwatch.",
        "price": 199.99,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
        "category_slug": "electronics",
        "stock": 30,
        "featured": True,
    },
    {
        "name": "Classic Denim Jacket",
        "description": "Timeless denim jacket made from premium cotton. Perfect for any casual occasion.",
        "price": 59.99,
        "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93b0?w=400",
        "category_slug": "clothing",
        "stock": 40,
        "featured": True,
    },
    {
        "name": "Running Sneakers",
        "description": "Lightweight running shoes with responsive cushioning for maximum comfort.",
        "price": 89.99,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "category_slug": "sports",
        "stock": 60,
        "featured": True,
    },
    {
        "name": "Ceramic Plant Pot Set",
        "description": "Set of 3 minimalist ceramic pots for indoor plants. Includes drainage trays.",
        "price": 34.99,
        "image": "https://images.unsplash.com/photo-1485955900006-10f4d324d411?w=400",
        "category_slug": "home-garden",
        "stock": 25,
        "featured": False,
    },
    {
        "name": "JavaScript: The Good Parts",
        "description": "Essential guide to the elegant, lightweight, and expressive features of JavaScript.",
        "price": 29.99,
        "image": "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400",
        "category_slug": "books",
        "stock": 100,
        "featured": False,
    },
    {
        "name": "Portable Bluetooth Speaker",
        "description": "Waterproof speaker with 360° sound and 12-hour playtime. Perfect for outdoor adventures.",
        "price": 49.99,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
        "category_slug": "electronics",
        "stock": 45,
        "featured": False,
    },
    {
        "name": "Yoga Mat Premium",
        "description": "Extra thick non-slip yoga mat with carrying strap. Eco-friendly TPE material.",
        "price": 39.99,
        "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
        "category_slug": "sports",
        "stock": 35,
        "featured": False,
    },
    {
        "name": "Cotton T-Shirt Pack",
        "description": "Pack of 3 soft cotton t-shirts in assorted colors. Comfortable everyday wear.",
        "price": 24.99,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        "category_slug": "clothing",
        "stock": 80,
        "featured": False,
    },
    {
        "name": "LED Desk Lamp",
        "description": "Adjustable LED desk lamp with touch controls and USB charging port.",
        "price": 44.99,
        "image": "https://images.unsplash.com/photo-1507473885765-e6ed423f92fe?w=400",
        "category_slug": "home-garden",
        "stock": 20,
        "featured": True,
    },
    {
        "name": "Design Patterns Book",
        "description": "Classic reference on object-oriented design patterns for software developers.",
        "price": 44.99,
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
        "category_slug": "books",
        "stock": 55,
        "featured": False,
    },
    {
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard with Cherry MX switches. Perfect for gaming and typing.",
        "price": 129.99,
        "image": "https://images.unsplash.com/photo-1511467687858-23d96c786e24?w=400",
        "category_slug": "electronics",
        "stock": 15,
        "featured": True,
    },
]


async def seed():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db]

    await db.categories.delete_many({})
    await db.products.delete_many({})

    category_map = {}
    for cat in CATEGORIES:
        result = await db.categories.insert_one(cat)
        category_map[cat["slug"]] = str(result.inserted_id)

    for product in PRODUCTS:
        slug = product.pop("category_slug")
        doc = {
            **product,
            "category_id": category_map[slug],
            "created_at": datetime.utcnow(),
        }
        await db.products.insert_one(doc)

    print(f"Seeded {len(CATEGORIES)} categories and {len(PRODUCTS)} products.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
