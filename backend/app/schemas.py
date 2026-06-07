from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    name: str
    is_admin: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class CategoryOut(BaseModel):
    id: str
    name: str
    slug: str


class ProductOut(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image: str
    category_id: str
    category_name: str | None = None
    stock: int
    featured: bool = False


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    price: float = Field(gt=0)
    image: str = ""
    category_id: str
    stock: int = Field(ge=0)
    featured: bool = False


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    image: str | None = None
    category_id: str | None = None
    stock: int | None = Field(default=None, ge=0)
    featured: bool | None = None


class CartItemIn(BaseModel):
    product_id: str
    quantity: int = Field(ge=1, le=99)


class CartItemOut(BaseModel):
    product_id: str
    name: str
    price: float
    image: str
    quantity: int
    subtotal: float


class CartOut(BaseModel):
    items: list[CartItemOut]
    total: float
    item_count: int


class OrderItemOut(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class OrderCreate(BaseModel):
    shipping_address: str = Field(min_length=5)
    phone: str = Field(min_length=5)


class OrderOut(BaseModel):
    id: str
    user_id: str
    items: list[OrderItemOut]
    total: float
    status: str
    shipping_address: str
    phone: str
    created_at: str
