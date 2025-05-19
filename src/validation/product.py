class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    sku: str
    price: float
    supplier_id: int
    stock: int