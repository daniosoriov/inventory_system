# Inventory Management System

A simple yet powerful inventory management system built with Python, FastAPI, PostgreSQL, and SQLAlchemy.
This application allows you to manage products, suppliers, and inventory stock through both a
RESTful API and a command-line interface.

## Features

- **RESTful API with FastAPI**
    - Modern, fast API with automatic OpenAPI documentation
    - Intuitive endpoint structure for all operations
    - Proper HTTP status codes and error responses

- **Supplier Management**
    - Create, retrieve, update, and delete suppliers via API endpoints
    - Track supplier details (name, email, phone number)

- **Product Management**
    - Create, retrieve, update, and delete products via API endpoints
    - Track product details (name, description, SKU, price)
    - Associate products with suppliers

- **Inventory Stock Tracking**
    - Track stock quantities for each product
    - Record inventory changes with transaction history
    - Support different operation types (ADD, SUBTRACT, SALE)

- **Robust Error Handling**
    - Comprehensive logging system
    - Exception handling with detailed error messages
    - Structured JSON responses for errors

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/daniosoriov/inventory_system.git
   cd inventory_system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:
    - Install PostgreSQL if not already installed
    - Create a database named `inventory`

5. Configure environment variables:
    - Create an `.env` file and fill in your database credentials:
      ```
      DB_USER='your_username'
      DB_PASS='your_password'
      DB_HOST='your_host'
      DB_PORT='your_port'
      DB_NAME='inventory'
      ```

6. Initialize the database:
   ```
   python -c "from src.orm_setup import setup_database; setup_database()"
   ```

## API Usage

The application provides a RESTful API built with FastAPI for managing inventory. You can interact with the API using
any HTTP client.

### Running the API Server

```bash
# Start the FastAPI server
fastapi run src/main.py --host
```

The API will be available at `http://localhost:8000`.

### API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### Supplier Management

```bash
# Create a new supplier
POST /suppliers/
{
  "name": "Supplier A",
  "email": "supplier@example.com",
  "phone_number": "+123456789"
}

# Get supplier details
GET /suppliers/1

# Update supplier details
PUT /suppliers/1
{
  "name": "Updated Supplier",
  "email": "new_email@example.com",
  "phone_number": "+123456789"
}

# Delete a supplier
DELETE /suppliers/1
```

#### Product Management

```bash
# Create a new product
POST /products/
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "sku": "LTP123",
  "price": 1500,
  "supplier_id": 1,
  "stock": 10
}

# Get product details
GET /products/1

# Update product details
PUT /products/1
{
  "name": "Updated Laptop",
  "description": "High-performance laptop",
  "sku": "LTP123",
  "price": 1600
}

# Delete a product
DELETE /products/1
```

#### Inventory Management

```bash
# Update product stock (add, subtract, or record a sale)
PUT /products/1/stock
{
  "quantity": 20,
  "operation": "SALE"
}
```

### Command-Line Interface

The application also provides a command-line interface for managing inventory. Here are some example commands:

```bash
# Create a new supplier
python src/cli.py create_supplier --name "Supplier A" --email "supplier@example.com" --phone_number "+123456789"

# Create a new product
python src/cli.py create_product --name "Laptop" --description "High-performance laptop" --sku "LTP123" --price 1500 --supplier_id 1 --stock 10

# Update product stock
python src/cli.py update_stock --product_id 1 --quantity 20 --operation ADD
```

## Project Structure

```
inventory_system/
├── logs/                  # Log files directory
│   └── logs.log           # Application logs
├── src/
│   ├── crud/              # CRUD operations
│   │   ├── __init__.py
│   │   ├── product.py     # Product CRUD operations
│   │   └── supplier.py    # Supplier CRUD operations
│   ├── routes/            # FastAPI route definitions
│   │   ├── __init__.py
│   │   ├── product.py     # Product API endpoints
│   │   └── supplier.py    # Supplier API endpoints
│   ├── validation/        # Pydantic models for validation
│   │   ├── __init__.py
│   │   ├── product.py     # Product validation models
│   │   └── supplier.py    # Supplier validation models
│   ├── utils/             # Utility functions
│   │   └── db.py          # Database utility functions
│   ├── cli.py             # Command-line interface
│   ├── database.py        # Database connection
│   ├── decorators.py      # Error handling decorators
│   ├── logger.py          # Logging configuration
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # SQLAlchemy ORM models
│   └── orm_setup.py       # Database connection setup
├── .env                   # Environment variables
├── README.md              # Project documentation
└── requirements.txt       # Project dependencies
```

## Data Models

### Supplier

- **id**: Unique identifier (primary key)
- **name**: Supplier name
- **email**: Supplier email (unique, indexed)
- **phone_number**: Supplier phone number
- **products**: Relationship to associated products

### Product

- **id**: Unique identifier (primary key)
- **name**: Product name
- **description**: Product description
- **sku**: Stock-keeping unit (unique, indexed)
- **price**: Product price
- **supplier_id**: Foreign key to supplier
- **stock**: Current stock quantity
- **supplier**: Relationship to supplier
- **transactions**: Relationship to associated transactions

### ProductTransaction

- **id**: Unique identifier (primary key)
- **product_id**: Foreign key to product
- **operation**: Type of operation (ADD, SUBTRACT, SALE)
- **quantity**: Quantity affected
- **date**: Transaction date and time
- **product**: Relationship to product

## Error Handling

The application uses a custom decorator (`handle_exceptions`) to handle exceptions consistently across the codebase. All
operations are logged to both the console and a log file for easy debugging and auditing.

## Configuration

The application uses environment variables for configuration. These are loaded from a `.env` file in the project root.
See the Installation section for details on setting up the environment variables.

## License

MIT License.
