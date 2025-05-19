from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from orm_setup import SessionLocal
from crud import get_supplier, create_supplier as create_supplier_crud, update_supplier as update_supplier_crud
from validation import SupplierCreate, SupplierUpdate, Supplier

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/suppliers/{supplier_id}")
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = get_supplier(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"supplier": supplier}


@app.post("/suppliers/")
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)) -> Supplier:
    try:
        result = create_supplier_crud(db, name=supplier.name, email=supplier.email, phone_number=supplier.phone_number)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/suppliers/{supplier_id}")
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    updated = update_supplier_crud(db, supplier_id, supplier.name, supplier.email, supplier.phone_number)
    db.commit()
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {'message': 'Supplier updated successfully'}
