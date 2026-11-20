# This file handles all Order endpoints (checkout, list orders, get order)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CartItem, Order, OrderItem, Product
from app.schemas import OrderResponse

# Create a router for order endpoints
router = APIRouter(prefix="/orders", tags=["Orders"])


# Checkout — turn the entire cart into an order
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def checkout(db: Session = Depends(get_db)):
    # Get all items in the cart
    cart_items = db.query(CartItem).all()

    # Can't checkout with an empty cart
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Create a new order (total_price will be calculated below)
    order = Order(total_price=0)
    db.add(order)

    total = 0.0

    # Go through each cart item and create an order item for it
    for cart_item in cart_items:
        # Look up the product to get its current price
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()

        # Create an order item with the product's current price and quantity
        order_item = OrderItem(
            order=order,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=product.price,
        )
        db.add(order_item)

        # Add to the running total
        total += product.price * cart_item.quantity

        # Reduce the product's stock by the ordered quantity
        product.stock -= cart_item.quantity

    # Set the final total price on the order
    order.total_price = total

    # Delete all cart items since they are now part of the order
    db.query(CartItem).delete()

    # Save everything to the database in one go
    db.commit()
    db.refresh(order)
    return order


# Get a list of all orders
@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


# Get a single order by its ID, including its items
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    # Try to find the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
