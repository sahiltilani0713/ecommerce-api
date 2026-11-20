# This file handles all Product endpoints (create, list, get, update, delete)

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category, Product
from app.schemas import ProductCreate, ProductUpdate, ProductResponse

# Create a router for product endpoints
router = APIRouter(prefix="/products", tags=["Products"])


# Create a new product
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Make sure the category exists before creating the product
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Create the product and save it to the database
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Get a list of products with optional pagination and category filter
@router.get("/", response_model=list[ProductResponse])
def list_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # Start building the query
    query = db.query(Product)

    # If a category_id was provided, filter by it
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    # Apply skip and limit for pagination
    return query.offset(skip).limit(limit).all()


# Get a single product by its ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    # Try to find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Update a product — only the fields that were sent get changed
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updates: ProductUpdate, db: Session = Depends(get_db)):
    # Try to find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Get only the fields the client actually sent (ignore missing ones)
    update_data = updates.model_dump(exclude_unset=True)

    # Apply each updated field to the product
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# Delete a product by its ID
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Try to find the product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Remove it from the database
    db.delete(product)
    db.commit()
