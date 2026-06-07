from fastapi import APIRouter

from app.redis_client import cache_get, cache_set
from app.database import get_db
from app.schemas import CategoryOut
from app.utils import serialize_docs

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
async def list_categories():
    cached = await cache_get("categories:all")
    if cached:
        return cached

    categories = serialize_docs(await get_db().categories.find().sort("name", 1).to_list(100))
    await cache_set("categories:all", categories, ttl=600)
    return categories
