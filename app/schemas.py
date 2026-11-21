# This file defines the shapes of data going in and out of the API using Pydantic

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# --- Category Schemas ---

# What the client sends when creating a new category
class CategoryCreate(BaseModel):
    name: str


# What the API sends back for a category
class CategoryResponse(BaseModel):
    id: int
    name: str

    # Tells Pydantic to read data from SQLAlchemy model attributes
    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

# What the client sends when registering a new user
class UserCreate(BaseModel):
    email: str
    # Password must be at least 6 characters
    password: str = Field(min_length=6)


# What the API sends back for a user (no password!)
class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# --- Token Schema ---

# The JWT token returned after login
class Token(BaseModel):
    access_token: str
    token_type: str


# --- Product Schemas ---

# What the client sends when creating a new product
class ProductCreate(BaseModel):
    name: str
    # Description is optional
    description: Optional[str] = None
    # Price must be greater than 0
    price: float = Field(gt=0)
    # Stock must be 0 or more
    stock: int = Field(ge=0, default=0)
    # Which category this product belongs to
    category_id: int


# What the client sends when updating a product — all fields are optional
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None


# What the API sends back for a product
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

# What the client sends when registering a new user
class UserCreate(BaseModel):
    email: str
    # Password must be at least 6 characters
    password: str = Field(min_length=6)


# What the API sends back for a user (no password!)
class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# --- Token Schema ---

# The JWT token returned after login
class Token(BaseModel):
    access_token: str
    token_type: str


# --- CartItem Schemas ---

# What the client sends when adding an item to the cart
class CartItemCreate(BaseModel):
    product_id: int
    # Must add at least 1 item
    quantity: int = Field(ge=1, default=1)


# What the API sends back for a cart item
class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

# What the client sends when registering a new user
class UserCreate(BaseModel):
    email: str
    # Password must be at least 6 characters
    password: str = Field(min_length=6)


# What the API sends back for a user (no password!)
class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# --- Token Schema ---

# The JWT token returned after login
class Token(BaseModel):
    access_token: str
    token_type: str


# --- Order Schemas ---

# What the API sends back for a single item inside an order
class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

# What the client sends when registering a new user
class UserCreate(BaseModel):
    email: str
    # Password must be at least 6 characters
    password: str = Field(min_length=6)


# What the API sends back for a user (no password!)
class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# --- Token Schema ---

# The JWT token returned after login
class Token(BaseModel):
    access_token: str
    token_type: str


# What the API sends back for a full order, including its items
class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime
    # List of items in this order
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

# What the client sends when registering a new user
class UserCreate(BaseModel):
    email: str
    # Password must be at least 6 characters
    password: str = Field(min_length=6)


# What the API sends back for a user (no password!)
class UserResponse(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# --- Token Schema ---

# The JWT token returned after login
class Token(BaseModel):
    access_token: str
    token_type: str
