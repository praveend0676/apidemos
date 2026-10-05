# 🛒 Order Management API Using Python & FastAPI

A beginner-friendly **Order Management REST API** built using **Python, FastAPI, Pydantic, SQLAlchemy, and SQLite**.

This project demonstrates how to build a real-world backend application where customers can view products, place orders, and track the order status.

The application also demonstrates important backend concepts such as:

* REST APIs
* FastAPI
* Pydantic validation
* SQLAlchemy ORM
* Database relationships
* Dependency Injection
* HTTP status codes
* Exception handling
* Server-side business logic
* Stock validation
* Order total calculation
* Order status workflow

---

# 📌 Problem Statement

Build a small FastAPI backend for placing and managing orders.

The application should provide APIs to:

```text
POST /products
GET /products

POST /orders
GET /orders
GET /orders/{order_id}

PUT /orders/{order_id}/status
```

An order should contain:

* Customer
* Products
* Quantities
* Total amount
* Order status

The order status should follow this workflow:

```text
PLACED
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED
```

The application must also:

1. Validate that the requested product exists.
2. Validate that quantity is greater than zero.
3. Validate available product stock.
4. Calculate the total order amount on the server.
5. Never trust the final amount supplied by the client.
6. Return meaningful HTTP errors.
7. Prevent invalid order-status transitions.

---

# 🎯 Project Objective

The main objective is to understand how a real-world FastAPI backend works from request to database.

The complete flow is:

```text
Client
   ↓
HTTP Request
   ↓
FastAPI Endpoint
   ↓
Pydantic Validation
   ↓
Business Logic
   ↓
SQLAlchemy ORM
   ↓
SQLite Database
   ↓
HTTP Response
```

---

# 🏗️ Application Architecture

```text
                    Client
                      │
                      ↓
                 FastAPI API
                      │
             ┌────────┴────────┐
             ↓                 ↓
       Pydantic Schema     Dependency
             │                 │
             ↓                 ↓
        Validation         DB Session
             │                 │
             └────────┬────────┘
                      ↓
                Business Logic
                      │
                      ↓
                SQLAlchemy ORM
                      │
                      ↓
                SQLite Database
```

---

# 📁 Project Structure

```text
order-management-api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── .gitignore
├── README.md
└── orders.db
```

> `orders.db` is generated automatically when the application runs and should normally be excluded from Git using `.gitignore`.

---

# 📄 File Responsibilities

## `main.py`

Contains:

* FastAPI application
* API endpoints
* Business logic
* Validation errors
* Order creation
* Order total calculation
* Stock updates
* Order status transitions

---

## `database.py`

Contains:

* Database URL
* SQLAlchemy engine
* Session factory
* Base class
* Database dependency

---

## `models.py`

Contains the SQLAlchemy database models:

```text
Product
Order
OrderItem
```

---

## `schemas.py`

Contains Pydantic request and response schemas.

It is responsible for validating API input and formatting API responses.

---

# 🗄️ Database Design

The application uses SQLite.

```text
                    Product
                       │
                       │
                       ↓
                  OrderItem
                       ↑
                       │
                       │
                     Order
```

---

# 📦 Product Table

The Product table contains:

```text
Product
├── id
├── name
├── description
├── price
└── stock
```

Example:

```json
{
    "id": 1,
    "name": "Laptop",
    "description": "Dell Inspiron Laptop",
    "price": 50000,
    "stock": 10
}
```

---

# 🧾 Order Table

The Order table contains:

```text
Order
├── id
├── customer
├── total_amount
└── status
```

Example:

```json
{
    "id": 1,
    "customer": "Praveen",
    "total_amount": 101000,
    "status": "PLACED"
}
```

---

# 🛍️ OrderItem Table

An order can contain multiple products.

For example:

```text
Order #1

├── Laptop × 2
├── Mouse × 1
└── Keyboard × 1
```

Therefore, the `OrderItem` table stores:

```text
OrderItem
├── id
├── order_id
├── product_id
├── quantity
└── unit_price
```

---

# 🔗 Database Relationship

```text
Product
   │
   │ 1
   │
   │
   │ Many
   ↓
OrderItem
   ↑
   │ Many
   │
   │ 1
   │
Order
```

An order can have many order items.

A product can appear in many order items.

---

# ⚙️ Technologies Used

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Programming language |
| FastAPI    | Web API framework    |
| Pydantic   | Data validation      |
| SQLAlchemy | ORM                  |
| SQLite     | Database             |
| Uvicorn    | ASGI server          |
| Swagger UI | API testing          |

---

# 🐍 Python Version

Recommended:

```text
Python 3.10+
```

---

# 🚀 Installation

## Step 1 — Create Project Folder

```powershell
mkdir order-management-api
cd order-management-api
```

---

# Step 2 — Create Virtual Environment

```powershell
python -m venv .venv
```

---

# Step 3 — Activate Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is not required in your environment, you can also run Python directly from the virtual environment.

Verify:

```powershell
python --version
```

---

# Step 4 — Install Dependencies

Create:

```text
requirements.txt
```

Add:

```text
fastapi
uvicorn[standard]
sqlalchemy
pydantic
```

Install:

```powershell
pip install -r requirements.txt
```

---

# ▶️ Running the Application

Start the FastAPI server:

```powershell
uvicorn main:app --reload
```

Expected output:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# 📖 Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to execute and test all APIs directly from the browser.

---

# 📚 ReDoc

FastAPI also provides ReDoc automatically:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔌 API Documentation

## 1. Create Product

### Endpoint

```http
POST /products
```

### Request

```json
{
    "name": "Laptop",
    "description": "Dell Inspiron Laptop",
    "price": 50000,
    "stock": 10
}
```

### Response

```json
{
    "id": 1,
    "name": "Laptop",
    "description": "Dell Inspiron Laptop",
    "price": 50000,
    "stock": 10
}
```

### Status Code

```text
201 Created
```

---

# 2. Get All Products

### Endpoint

```http
GET /products
```

### Example Response

```json
[
    {
        "id": 1,
        "name": "Laptop",
        "description": "Dell Inspiron Laptop",
        "price": 50000,
        "stock": 10
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "description": "Bluetooth Mouse",
        "price": 1000,
        "stock": 20
    }
]
```

### Status Code

```text
200 OK
```

---

# 3. Create Order

### Endpoint

```http
POST /orders
```

### Request

```json
{
    "customer": "Praveen",
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        },
        {
            "product_id": 2,
            "quantity": 1
        }
    ]
}
```

---

# 💰 Server-Side Total Calculation

The client sends:

```text
Product ID
Quantity
```

The client does **not** send:

```text
Total Amount
```

The server retrieves the product price from the database.

For example:

```text
Laptop
Price = ₹50,000
Quantity = 2

₹50,000 × 2
= ₹1,00,000
```

Mouse:

```text
Price = ₹1,000
Quantity = 1

₹1,000 × 1
= ₹1,000
```

Total:

```text
₹1,00,000
+
₹1,000
----------------
₹1,01,000
```

The server stores:

```json
{
    "total_amount": 101000
}
```

This prevents the client from simply submitting an arbitrary final amount.

---

# 📤 Create Order Response

```json
{
    "id": 1,
    "customer": "Praveen",
    "total_amount": 101000,
    "status": "PLACED",
    "items": [
        {
            "id": 1,
            "product_id": 1,
            "quantity": 2,
            "unit_price": 50000
        },
        {
            "id": 2,
            "product_id": 2,
            "quantity": 1,
            "unit_price": 1000
        }
    ]
}
```

### Status Code

```text
201 Created
```

---

# 4. Get All Orders

### Endpoint

```http
GET /orders
```

Example:

```json
[
    {
        "id": 1,
        "customer": "Praveen",
        "total_amount": 101000,
        "status": "PLACED"
    }
]
```

---

# 5. Get Specific Order

### Endpoint

```http
GET /orders/{order_id}
```

Example:

```http
GET /orders/1
```

Response:

```json
{
    "id": 1,
    "customer": "Praveen",
    "total_amount": 101000,
    "status": "PLACED"
}
```

---

# 6. Update Order Status

### Endpoint

```http
PUT /orders/{order_id}/status
```

Example:

```http
PUT /orders/1/status
```

Request:

```json
{
    "status": "PROCESSING"
}
```

Response:

```json
{
    "id": 1,
    "customer": "Praveen",
    "total_amount": 101000,
    "status": "PROCESSING"
}
```

---

# 🔄 Order Status Workflow

The application follows this workflow:

```text
        PLACED
           │
           ↓
      PROCESSING
           │
           ↓
        SHIPPED
           │
           ↓
       DELIVERED
```

Valid transitions:

```text
PLACED → PROCESSING

PROCESSING → SHIPPED

SHIPPED → DELIVERED
```

Invalid transitions are rejected.

For example:

```text
PLACED → SHIPPED
```

is not allowed.

---

# ❌ Error Handling

The application returns meaningful HTTP errors.

---

## Product Not Found

Request:

```json
{
    "customer": "Praveen",
    "items": [
        {
            "product_id": 999,
            "quantity": 1
        }
    ]
}
```

Response:

```text
404 Not Found
```

```json
{
    "detail": "Product 999 not found"
}
```

---

# ❌ Invalid Quantity

Example:

```json
{
    "product_id": 1,
    "quantity": -5
}
```

The Pydantic schema uses:

```python
quantity: int = Field(gt=0)
```

Therefore:

```text
quantity > 0
```

is required.

FastAPI returns a validation error.

---

# ❌ Insufficient Stock

Suppose:

```text
Available stock = 5
```

Customer requests:

```text
Quantity = 10
```

The API returns:

```text
400 Bad Request
```

Example:

```json
{
    "detail": "Insufficient stock for product 1. Available stock: 5"
}
```

---

# ❌ Order Not Found

Request:

```http
GET /orders/999
```

Response:

```text
404 Not Found
```

```json
{
    "detail": "Order 999 not found"
}
```

---

# ❌ Invalid Status Transition

Suppose the current status is:

```text
PLACED
```

Trying to change directly to:

```text
SHIPPED
```

is invalid.

The API returns:

```text
400 Bad Request
```

Example:

```json
{
    "detail": "Invalid status transition. PLACED can only move to PROCESSING"
}
```

---

# 🧪 Complete Testing Flow

Use Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Test APIs in this order:

```text
1. POST /products
        ↓
2. POST /products
        ↓
3. GET /products
        ↓
4. POST /orders
        ↓
5. GET /orders
        ↓
6. GET /orders/{order_id}
        ↓
7. PUT /orders/{order_id}/status
        ↓
8. PUT /orders/{order_id}/status
        ↓
9. PUT /orders/{order_id}/status
```

---

# 🧪 Negative Testing

Also demonstrate:

```text
1. Invalid product ID
        ↓
404

2. Negative quantity
        ↓
422 Validation Error

3. Quantity greater than stock
        ↓
400

4. Invalid order ID
        ↓
404

5. Invalid status transition
        ↓
400
```

---

# 🔐 Important Business Rule

The most important rule in this application is:

> **Never accept the final order amount directly from the client.**

Incorrect approach:

```json
{
    "customer": "Praveen",
    "total_amount": 10
}
```

The server should not blindly trust this value.

Correct approach:

```text
Client
  │
  ├── Product ID
  └── Quantity
         │
         ↓
      Server
         │
         ↓
   Database Product
         │
         ↓
      Price
         │
         ×
      Quantity
         │
         ↓
    Total Amount
```

---

# 🧠 OOP / Backend Concepts Demonstrated

| Concept              | Demonstration                   |
| -------------------- | ------------------------------- |
| Python               | Application language            |
| FastAPI              | REST API framework              |
| Pydantic             | Request validation              |
| SQLAlchemy           | ORM                             |
| SQLite               | Database                        |
| Dependency Injection | `Depends(get_db)`               |
| CRUD                 | Product and order APIs          |
| Relationships        | Order → OrderItem → Product     |
| HTTP Methods         | GET, POST, PUT                  |
| HTTP Status Codes    | 200, 201, 400, 404, 422         |
| Exception Handling   | `HTTPException`                 |
| Business Logic       | Total and stock calculation     |
| Validation           | Product and quantity validation |
| State Management     | Order status workflow           |

---

# 🧩 Complete Application Flow

```text
                   CLIENT
                      │
                      ↓
               POST /products
                      │
                      ↓
               Pydantic Validation
                      │
                      ↓
                 SQLAlchemy
                      │
                      ↓
                SQLite Database
                      │
                      ↓
                  PRODUCT
                      │
                      │
                      ↓
                POST /orders
                      │
                      ↓
              Validate Product
                      │
                      ↓
              Validate Quantity
                      │
                      ↓
               Validate Stock
                      │
                      ↓
             Get Product Price
                      │
                      ↓
              Calculate Total
                      │
                      ↓
                Create Order
                      │
                      ↓
                  PLACED
                      │
                      ↓
                 PROCESSING
                      │
                      ↓
                  SHIPPED
                      │
                      ↓
                 DELIVERED
```

---

# 🎥 YouTube Video Demonstration

The recommended video sequence is:

## Part 1 — Introduction

Explain:

* What is an API?
* What is FastAPI?
* What problem are we solving?
* What is an Order Management System?

---

## Part 2 — Problem Statement

Explain:

```text
Products
Orders
Order Items
Order Status
```

Explain the required APIs:

```text
POST /products
GET /products
POST /orders
GET /orders
GET /orders/{order_id}
PUT /orders/{order_id}/status
```

---

## Part 3 — Project Structure

Show:

```text
main.py
database.py
models.py
schemas.py
requirements.txt
README.md
```

Explain the responsibility of every file.

---

## Part 4 — Database

Explain:

```text
Product
Order
OrderItem
```

Show the relationships.

---

## Part 5 — Pydantic Validation

Explain:

```python
Field(gt=0)
```

and:

```python
Field(ge=0)
```

Explain why validation should happen before business processing.

---

## Part 6 — Product APIs

Demonstrate:

```text
POST /products
GET /products
```

---

## Part 7 — Order Creation

Demonstrate:

```text
POST /orders
```

Explain:

```text
Product Price
     ×
Quantity
     ↓
Item Amount
     ↓
Order Total
```

Emphasize that the client does not provide the total amount.

---

## Part 8 — Order Retrieval

Demonstrate:

```text
GET /orders
```

and:

```text
GET /orders/{order_id}
```

---

## Part 9 — Order Status

Demonstrate:

```text
PLACED
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED
```

---

## Part 10 — Error Handling

Demonstrate:

```text
Invalid Product
      ↓
404

Invalid Quantity
      ↓
422

Insufficient Stock
      ↓
400

Invalid Order
      ↓
404

Invalid Status Transition
      ↓
400
```

---

# 📝 Example Real-World Scenario

Imagine an online shopping application.

A customer named **Praveen** wants to buy:

```text
2 × Laptop
1 × Wireless Mouse
```

The customer sends:

```json
{
    "customer": "Praveen",
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        },
        {
            "product_id": 2,
            "quantity": 1
        }
    ]
}
```

The backend retrieves the prices:

```text
Laptop = ₹50,000
Mouse  = ₹1,000
```

The backend calculates:

```text
₹50,000 × 2 = ₹1,00,000

₹1,000 × 1 = ₹1,000

Total = ₹1,01,000
```

The order is created as:

```text
PLACED
```

The order can then progress:

```text
PLACED
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED
```

This represents a simplified real-world e-commerce order workflow.

---

# 📌 API Summary

| Method | Endpoint                    | Description    | Success |
| ------ | --------------------------- | -------------- | ------- |
| POST   | `/products`                 | Create product | 201     |
| GET    | `/products`                 | List products  | 200     |
| POST   | `/orders`                   | Create order   | 201     |
| GET    | `/orders`                   | List orders    | 200     |
| GET    | `/orders/{order_id}`        | Get order      | 200     |
| PUT    | `/orders/{order_id}/status` | Update status  | 200     |

---

# ▶️ Quick Start

```powershell
python -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install:

```powershell
pip install -r requirements.txt
```

Run:

```powershell
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---
---

# ⭐ Key Takeaways

```text
FastAPI
   ↓
API Endpoints
   ↓
Pydantic Validation
   ↓
Business Logic
   ↓
SQLAlchemy
   ↓
SQLite
```

And for order processing:

```text
Product
   ↓
Quantity
   ↓
Validate
   ↓
Get Price
   ↓
Calculate Total
   ↓
Create Order
   ↓
PLACED
   ↓
PROCESSING
   ↓
SHIPPED
   ↓
DELIVERED
```

---

# 📚 Final Summary

This project demonstrates a complete beginner-level backend application using Python and FastAPI.

The application manages:

```text
Products
   +
Orders
   +
Order Items
   +
Stock
   +
Order Status
```

The most important design principle demonstrated is:

> **The server owns the business logic and calculates the final order amount using trusted product prices stored in the database.**

The project provides a practical introduction to building REST APIs with FastAPI and connecting those APIs to a relational database using SQLAlchemy.

---

