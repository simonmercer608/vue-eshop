import json
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.redis_client import get_redis
from app.schemas import CartItemIn, CartItemOut, CartOut
from app.utils import serialize_doc

router = APIRouter(prefix="/cart", tags=["cart"])


def cart_key(user_id: str) -> str:
    return f"cart:{user_id}"


async def load_cart(user_id: str) -> dict[str, int]:
    raw = await get_redis().get(cart_key(user_id))
    if not raw:
        return {}
    return json.loads(raw)


async def save_cart(user_id: str, cart: dict[str, int]) -> None:
    if cart:
        await get_redis().set(cart_key(user_id), json.dumps(cart), ex=settings.cart_ttl_seconds)
    else:
        await get_redis().delete(cart_key(user_id))


async def build_cart_response(user_id: str) -> CartOut:
    cart = await load_cart(user_id)
    if not cart:
        return CartOut(items=[], total=0, item_count=0)

    items: list[CartItemOut] = []
    total = 0.0
    item_count = 0

    for product_id, quantity in cart.items():
        product = serialize_doc(await get_db().products.find_one({"_id": ObjectId(product_id)}))
        if not product:
            continue
        subtotal = product["price"] * quantity
        items.append(
            CartItemOut(
                product_id=product["id"],
                name=product["name"],
                price=product["price"],
                image=product.get("image", ""),
                quantity=quantity,
                subtotal=subtotal,
            )
        )
        total += subtotal
        item_count += quantity

    return CartOut(items=items, total=round(total, 2), item_count=item_count)


@router.get("", response_model=CartOut)
async def get_cart(current_user: Annotated[dict, Depends(get_current_user)]):
    return await build_cart_response(current_user["id"])


@router.post("/items", response_model=CartOut)
async def add_to_cart(data: CartItemIn, current_user: Annotated[dict, Depends(get_current_user)]):
    product = await get_db().products.find_one({"_id": ObjectId(data.product_id)})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.get("stock", 0) < data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")

    cart = await load_cart(current_user["id"])
    cart[data.product_id] = cart.get(data.product_id, 0) + data.quantity
    await save_cart(current_user["id"], cart)
    return await build_cart_response(current_user["id"])


@router.put("/items/{product_id}", response_model=CartOut)
async def update_cart_item(
    product_id: str,
    quantity: int,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    if quantity < 1 or quantity > 99:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be 1-99")

    product = await get_db().products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.get("stock", 0) < quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")

    cart = await load_cart(current_user["id"])
    if product_id not in cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")

    cart[product_id] = quantity
    await save_cart(current_user["id"], cart)
    return await build_cart_response(current_user["id"])


@router.delete("/items/{product_id}", response_model=CartOut)
async def remove_cart_item(product_id: str, current_user: Annotated[dict, Depends(get_current_user)]):
    cart = await load_cart(current_user["id"])
    cart.pop(product_id, None)
    await save_cart(current_user["id"], cart)
    return await build_cart_response(current_user["id"])


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(current_user: Annotated[dict, Depends(get_current_user)]):
    await save_cart(current_user["id"], {})
