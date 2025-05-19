from pydantic import BaseModel
from models import OperationType


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    sku: str
    price: float
    supplier_id: int
    stock: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'Product Name',
                    'description': 'Product Description',
                    'sku': 'SKU12345',
                    'price': 19.99,
                    'supplier_id': 1,
                    'stock': 100
                }
            ]
        }
    }


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    sku: str | None = None
    price: float | None = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'name': 'Updated Product Name',
                    'description': 'Updated Product Description',
                    'sku': 'SKU12345',
                    'price': 19.99,
                }
            ]
        }
    }


class ProductUpdateStock(BaseModel):
    quantity: int
    operation: OperationType

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'quantity': 10,
                    'operation': OperationType.SALE
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
