# E-commerce API

A minimal e-commerce backend built with FastAPI and SQLite.  
Supports categories, products, cart, and checkout with stock management.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM for database operations
- **SQLite** — lightweight file-based database
- **Pydantic v2** — request/response validation
- **Uvicorn** — ASGI server

## Features

- Category CRUD (create, list, get, delete)
- Product CRUD with pagination (`skip`, `limit`) and category filter
- Cart management (add items, increase quantity if already in cart, remove items)
- Checkout — converts cart to an order, copies product prices, calculates total, reduces stock, and clears the cart

## Project Structure

```
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── database.py         # SQLite engine, session, get_db dependency
│   ├── models.py           # SQLAlchemy table definitions
│   ├── schemas.py          # Pydantic request/response schemas
│   └── routers/
│       ├── __init__.py
│       ├── categories.py   # /categories endpoints
│       ├── products.py     # /products endpoints
│       ├── cart.py          # /cart endpoints
│       └── orders.py       # /orders endpoints
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup (Windows)

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** to see the interactive API docs.

## API Endpoints

### General

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |

### Categories

| Method | Path | Description |
|--------|------|-------------|
| POST | `/categories/` | Create a category |
| GET | `/categories/` | List all categories |
| GET | `/categories/{category_id}` | Get one category |
| DELETE | `/categories/{category_id}` | Delete a category |

### Products

| Method | Path | Description |
|--------|------|-------------|
| POST | `/products/` | Create a product |
| GET | `/products/` | List products (supports `skip`, `limit`, `category_id`) |
| GET | `/products/{product_id}` | Get one product |
| PUT | `/products/{product_id}` | Update a product (partial) |
| DELETE | `/products/{product_id}` | Delete a product |

### Cart

| Method | Path | Description |
|--------|------|-------------|
| POST | `/cart/` | Add item to cart (increases quantity if already in cart) |
| GET | `/cart/` | List all cart items |
| DELETE | `/cart/{item_id}` | Remove one cart item |

### Orders

| Method | Path | Description |
|--------|------|-------------|
| POST | `/orders/` | Checkout — create order from cart |
| GET | `/orders/` | List all orders |
| GET | `/orders/{order_id}` | Get one order with its items |

## What I Learned

- **Dependency injection with `Depends`** — FastAPI's `Depends(get_db)` gives each request its own database session and cleans it up automatically.
- **Pydantic validation** — using `Field(gt=0)` and `Field(ge=1)` to enforce rules like "price must be positive" at the schema level, before the code even runs.
- **Database transactions** — grouping multiple database changes (create order items, reduce stock, clear cart) into a single `commit()` so everything succeeds or fails together.
