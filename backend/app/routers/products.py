from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.dependencies import get_admin_user
from app.redis_client import cache_delete, cache_get, cache_set
from app.schemas import ProductCreate, ProductOut, ProductUpdate
from app.utils import serialize_doc, serialize_docs

router = APIRouter(prefix="/products", tags=["products"])


async def enrich_products(products: list[dict]) -> list[dict]:
    if not products:
        return []
    category_ids = list({p["category_id"] for p in products if p.get("category_id")})
    categories = {}
    if category_ids:
        cursor = get_db().categories.find({"_id": {"$in": [ObjectId(cid) for cid in category_ids]}})
        async for cat in cursor:
            categories[str(cat["_id"])] = cat["name"]
    for product in products:
        product["category_name"] = categories.get(product.get("category_id"))
    return products


@router.get("", response_model=list[ProductOut])
async def list_products(
    category: str | None = None,
    search: str | None = None,
    featured: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    cache_key = f"products:list:{category}:{search}:{featured}:{skip}:{limit}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    query: dict = {}
    if category:
        query["category_id"] = category
    if featured is not None:
        query["featured"] = featured
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
        ]

    products = serialize_docs(
        await get_db().products.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    )
    products = await enrich_products(products)
    await cache_set(cache_key, products, ttl=120)
    return products


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str):
    cache_key = f"products:detail:{product_id}"
    cached = await cache_get(cache_key)
    if cached:
        return cached

    product = serialize_doc(await get_db().products.find_one({"_id": ObjectId(product_id)}))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    enriched = (await enrich_products([product]))[0]
    await cache_set(cache_key, enriched, ttl=300)
    return enriched


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, _: Annotated[dict, Depends(get_admin_user)]):
    db = get_db()
    if not await db.categories.find_one({"_id": ObjectId(data.category_id)}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    doc = {
        **data.model_dump(),
        "created_at": __import__("datetime").datetime.utcnow(),
    }
    result = await db.products.insert_one(doc)
    product = serialize_doc({**doc, "_id": result.inserted_id})
    enriched = (await enrich_products([product]))[0]
    await cache_delete("categories:all")
    return enriched


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: str,
    data: ProductUpdate,
    _: Annotated[dict, Depends(get_admin_user)],
):
    db = get_db()
    updates = {k: v for k, v in data.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    if "category_id" in updates:
        if not await db.categories.find_one({"_id": ObjectId(updates["category_id"])}):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")

    result = await db.products.find_one_and_update(
        {"_id": ObjectId(product_id)},
        {"$set": updates},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = serialize_doc(result)
    enriched = (await enrich_products([product]))[0]
    await cache_delete(f"products:detail:{product_id}")
    return enriched


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, _: Annotated[dict, Depends(get_admin_user)]):
    result = await get_db().products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    await cache_delete(f"products:detail:{product_id}")
