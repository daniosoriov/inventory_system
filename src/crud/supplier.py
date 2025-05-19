from sqlalchemy.orm import Session
from decorators import handle_exceptions
from models import Supplier, Product, ProductTransaction, OperationType


@handle_exceptions()
def create_supplier(session: Session, name: str, email: str, phone_number: str) -> Supplier:
    new_supplier = Supplier(
        name=name,
        email=email,
        phone_number=phone_number
    )
    session.add(new_supplier)
    return new_supplier


@handle_exceptions()
def get_supplier(session: Session, supplier_id: int) -> Supplier | None:
    supplier = session.query(Supplier).filter_by(id=supplier_id).first()
    return supplier


@handle_exceptions()
def update_supplier(session: Session, supplier_id: int, name: str = None, email: str = None,
                    phone_number: str = None) -> Supplier | None:
    supplier = session.query(Supplier).filter_by(id=supplier_id).first()
    if not supplier:
        return None
    if name:
        supplier.name = name
    if email:
        supplier.email = email
    if phone_number:
        supplier.phone_number = phone_number
    return supplier


@handle_exceptions()
def delete_supplier(session: Session, supplier_id: int) -> bool:
    supplier = session.query(Supplier).filter_by(id=supplier_id).first()
    if supplier:
        session.delete(supplier)
        return True
    return False
