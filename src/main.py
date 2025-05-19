from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from orm_setup import SessionLocal
from crud import get_supplier, create_supplier as create_supplier_crud
from validation import SupplierCreate, Supplier

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
    # @typing_extensions.deprecated('The `from_orm` method is deprecated; set '
    #         "`model_config['from_attributes']=True` and use `model_validate` instead.", category=None)
    try:
        result = create_supplier_crud(db, name=supplier.name, email=supplier.email, phone_number=supplier.phone_number)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
