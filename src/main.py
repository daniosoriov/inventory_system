import logging.config

from fastapi import FastAPI
from routes.supplier import router as supplier_router
from routes.product import router as product_router

from logger import LOGGING_CONF

logging.config.dictConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(supplier_router, prefix="/suppliers", tags=["suppliers"])
app.include_router(product_router, prefix="/products", tags=["products"])
