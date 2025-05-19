from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from crud.product import (get_product, create_product, update_product, delete_product, update_stock)
from validation.product import ProductCreate, ProductUpdate, ProductUpdateStock, Product
from utils.db import get_db

router = APIRouter()


@router.get("/{product_id}", name='Get Product')
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return {'product': product}


@router.post("/", name='Create Product')
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)) -> dict[str, Product]:
    try:
        result = create_product(db, name=product.name, description=product.description, sku=product.sku,
                                price=product.price, stock=product.stock, supplier_id=product.supplier_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'product': result}


@router.put("/{product_id}", name='Update Product')
def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_product(db, product_id, name=product.name, description=product.description,
                                 sku=product.sku, price=product.price)
        if not updated:
            raise HTTPException(status_code=404, detail="product not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'message': 'product updated successfully'}


@router.put("/{product_id}/stock", name='Update Product Stock')
def update_product_stock_endpoint(product_id: int, product: ProductUpdateStock, db: Session = Depends(get_db)):
    try:
        updated = update_stock(db, product_id, quantity=product.quantity, operation=product.operation)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="product not found")
    return {'message': 'product stock updated successfully'}


@router.delete("/{product_id}", name='Delete Product')
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    deleted = delete_product(db, product_id)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=404, detail="product not found")
    return {'message': 'product deleted successfully'}
