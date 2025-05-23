from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from crud.supplier import (get_supplier, create_supplier, update_supplier, delete_supplier)
from validation.supplier import SupplierCreate, SupplierUpdate, Supplier
from utils.db import get_db

router = APIRouter()


@router.get("/{supplier_id}", name='Get Supplier')
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {'supplier': supplier}


@router.post("/", name='Create Supplier')
def create_supplier_endpoint(supplier: SupplierCreate, db: Session = Depends(get_db)) -> dict[str, Supplier]:
    try:
        result = create_supplier(db, name=supplier.name, email=supplier.email, phone_number=supplier.phone_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'supplier': result}


@router.put("/{supplier_id}", name='Update Supplier')
def update_supplier_endpoint(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_supplier(db, supplier_id, supplier.name, supplier.email, supplier.phone_number)
        if not updated:
            raise HTTPException(status_code=404, detail="Supplier not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'message': 'Supplier updated successfully'}


@router.delete("/{supplier_id}", name='Delete Supplier')
def delete_supplier_endpoint(supplier_id: int, db: Session = Depends(get_db)):
    try:
        deleted = delete_supplier(db, supplier_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Supplier not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'message': 'Supplier deleted successfully'}
