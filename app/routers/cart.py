# This file handles all Cart endpoints (add item, list items, remove item)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CartItem, Product
from app.schemas import CartItemCreate, CartItemResponse

# Create a router for cart endpoints
router = APIRouter(prefix="/cart", tags=["Cart"])


# Add a product to the cart (or increase quantity if it's already there)
@router.post("/", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    # Make sure the product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the requested quantity is available in stock
    if item.quantity > product.stock:
        raise HTTPException(status_code=400, detail="Quantity exceeds available stock")

    # Check if this product is already in the cart
    existing = db.query(CartItem).filter(CartItem.product_id == item.product_id).first()

    if existing:
        # Product already in cart — just increase the quantity
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return existing

    # Product not in cart yet — create a new cart item
    db_item = CartItem(product_id=item.product_id, quantity=item.quantity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Get all items currently in the cart
@router.get("/", response_model=list[CartItemResponse])
def list_cart(db: Session = Depends(get_db)):
    return db.query(CartItem).all()


# Remove a single item from the cart by its ID
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    # Try to find the cart item
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    # Remove it from the database
    db.delete(item)
    db.commit()
