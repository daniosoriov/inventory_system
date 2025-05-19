from pydantic import BaseModel


class SupplierCreate(BaseModel):
    name: str
    email: str
    phone_number: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'Supplier Name',
                    'email': 'test@test.com',
                    'phone_number': '+1234567890'
                }
            ]
        }
    }


class Supplier(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'id': 1,
                    'name': 'Supplier Name',
                    'email': 'test@test.com',
                    'phone_number': '+1234567890'
                }
            ]
        }
    }


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    sku: str
    price: float
    supplier_id: int
    stock: int

# class ProductTransaction(BaseModel):
#     id: int
#     product_id: int
#     quantity: int
#     operation_type: str  # Assuming this is a string, e.g., 'add' or 'subtract'
#     timestamp: str  # Assuming this is a string, e.g., ISO format
