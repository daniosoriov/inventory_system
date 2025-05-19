from fastapi import FastAPI
from routes.supplier import router as supplier_router
from routes.product import router as product_router

app = FastAPI()

app.include_router(supplier_router, prefix="/suppliers", tags=["suppliers"])
app.include_router(product_router, prefix="/products", tags=["products"])
