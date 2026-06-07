from datetime import datetime
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.dependencies import get_current_user
from app.routers.cart import build_cart_response, save_cart
from app.schemas import OrderCreate, OrderOut
from app.utils import serialize_doc, serialize_docs

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(data: OrderCreate, current_user: Annotated[dict, Depends(get_current_user)]):
    cart_response = await build_cart_response(current_user["id"])
    if not cart_response.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    db = get_db()
    order_items = []
    for item in cart_response.items:
        product = await db.products.find_one({"_id": ObjectId(item.product_id)})
        if not product or product.get("stock", 0) < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {item.name}",
            )
        await db.products.update_one(
            {"_id": ObjectId(item.product_id)},
            {"$inc": {"stock": -item.quantity}},
        )
        order_items.append(item.model_dump())

    order_doc = {
        "user_id": current_user["id"],
        "items": order_items,
        "total": cart_response.total,
        "status": "pending",
        "shipping_address": data.shipping_address,
        "phone": data.phone,
        "created_at": datetime.utcnow(),
    }
    result = await db.orders.insert_one(order_doc)
    await save_cart(current_user["id"], {})

    order = serialize_doc({**order_doc, "_id": result.inserted_id})
    order["created_at"] = order_doc["created_at"].isoformat()
    return OrderOut(**order)


@router.get("", response_model=list[OrderOut])
async def list_orders(current_user: Annotated[dict, Depends(get_current_user)]):
    orders = serialize_docs(
        await get_db().orders.find({"user_id": current_user["id"]}).sort("created_at", -1).to_list(50)
    )
    for order in orders:
        if isinstance(order.get("created_at"), datetime):
            order["created_at"] = order["created_at"].isoformat()
    return orders


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: str, current_user: Annotated[dict, Depends(get_current_user)]):
    order = serialize_doc(await get_db().orders.find_one({"_id": ObjectId(order_id)}))
    if not order or order["user_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if isinstance(order.get("created_at"), datetime):
        order["created_at"] = order["created_at"].isoformat()
    return OrderOut(**order)
