from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import Token, UserOut, UserRegister
from app.utils import create_access_token, hash_password, serialize_doc, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister):
    db = get_db()
    existing = await db.users.find_one({"email": data.email.lower()})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_count = await db.users.count_documents({})
    user_doc = {
        "email": data.email.lower(),
        "password": hash_password(data.password),
        "name": data.name,
        "is_admin": user_count == 0,
        "created_at": __import__("datetime").datetime.utcnow(),
    }
    result = await db.users.insert_one(user_doc)
    user = serialize_doc({**user_doc, "_id": result.inserted_id})
    token = create_access_token({"sub": user["id"]})
    return {
        "access_token": token,
        "user": UserOut(**user),
    }


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db = get_db()
    user = await db.users.find_one({"email": form_data.username.lower()})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_out = serialize_doc(user)
    token = create_access_token({"sub": user_out["id"]})
    return {
        "access_token": token,
        "user": UserOut(**user_out),
    }


@router.get("/me", response_model=UserOut)
async def me(current_user: Annotated[dict, Depends(get_current_user)]):
    return UserOut(**current_user)
