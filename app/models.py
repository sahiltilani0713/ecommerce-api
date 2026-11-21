# This file defines all database tables as Python classes using SQLAlchemy

from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

# Import the Base class that all models inherit from
from app.database import Base


# Category table — groups products into categories like "Electronics", "Clothing"
class Category(Base):
    __tablename__ = "categories"

    # Unique ID for each category
    id = Column(Integer, primary_key=True, index=True)
    # Category name, must be unique and not empty
    name = Column(String, unique=True, nullable=False)


# Product table — stores item details like name, price, and stock
class Product(Base):
    __tablename__ = "products"

    # Unique ID for each product
    id = Column(Integer, primary_key=True, index=True)
    # Product name, required
    name = Column(String, nullable=False)
    # Optional description of the product
    description = Column(String, nullable=True)
    # Price of the product, required
    price = Column(Float, nullable=False)
    # How many units are in stock, defaults to 0
    stock = Column(Integer, default=0)
    # Links this product to a category
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Lets us access the full Category object from a Product
    category = relationship("Category")


# CartItem table — holds items a customer has added to their cart
class CartItem(Base):
    __tablename__ = "cart_items"

    # Unique ID for each cart entry
    id = Column(Integer, primary_key=True, index=True)
    # Which product is in the cart
    product_id = Column(Integer, ForeignKey("products.id"))
    # How many of this product, defaults to 1
    quantity = Column(Integer, default=1)

    # Lets us access the full Product object from a CartItem
    product = relationship("Product")


# Order table — represents a completed or pending order
class Order(Base):
    __tablename__ = "orders"

    # Unique ID for each order
    id = Column(Integer, primary_key=True, index=True)
    # Total cost of the order
    total_price = Column(Float)
    # Order status like "pending", "shipped", "delivered"
    status = Column(String, default="pending")
    # When the order was created, defaults to current time
    created_at = Column(DateTime, default=datetime.utcnow)

    # Lets us access all OrderItems that belong to this order
    items = relationship("OrderItem", back_populates="order")


# OrderItem table — one line item inside an order (product + quantity + price)
class OrderItem(Base):
    __tablename__ = "order_items"

    # Unique ID for each order item
    id = Column(Integer, primary_key=True, index=True)
    # Which order this item belongs to
    order_id = Column(Integer, ForeignKey("orders.id"))
    # Which product was ordered
    product_id = Column(Integer, ForeignKey("products.id"))
    # How many units were ordered
    quantity = Column(Integer)
    # Price at the time of order (may differ from current product price)
    price = Column(Float)

    # Lets us go back to the parent Order from an OrderItem
    order = relationship("Order", back_populates="items")


# User table — stores registered user accounts
class User(Base):
    __tablename__ = "users"

    # Unique ID for each user
    id = Column(Integer, primary_key=True, index=True)
    # User's email, must be unique and not empty
    email = Column(String, unique=True, nullable=False, index=True)
    # Hashed version of the user's password (never store plain text)
    hashed_password = Column(String, nullable=False)
