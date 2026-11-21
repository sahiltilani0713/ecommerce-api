# Import FastAPI framework
from fastapi import FastAPI

# Import our database setup
from app.database import engine, Base

# Import models so SQLAlchemy knows about all tables before creating them
from app import models

# Import the routers for auth, categories, products, cart, and orders
from app.routers import auth, categories, products, cart, orders

# Create the FastAPI application with a title
app = FastAPI(title="E-commerce API")

# Create all database tables when the app starts
Base.metadata.create_all(bind=engine)

# Register all routers with the app
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)


# Root endpoint to check if the API is running
@app.get("/")
def root():
    return {"message": "E-commerce API is running"}
