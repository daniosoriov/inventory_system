import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from decorators import handle_exceptions
from models import Supplier

logger = logging.getLogger()


@handle_exceptions()
def create_supplier(session: Session, name: str, email: str, phone_number: str) -> Supplier:
    try:
        new_supplier = Supplier(
            name=name,
            email=email,
            phone_number=phone_number
        )
        session.add(new_supplier)
        session.commit()
        session.refresh(new_supplier)
        return new_supplier
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Supplier with email {email} already exists.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating supplier: {e}")
        raise ValueError("An error occurred while creating the supplier.")


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

    try:
        if name:
            supplier.name = name
        if email:
            supplier.email = email
        if phone_number:
            supplier.phone_number = phone_number
        session.commit()
        session.refresh(supplier)
        return supplier
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Supplier with email {email} already exists.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating supplier: {e}")
        raise ValueError("An error occurred while updating the supplier.")


@handle_exceptions()
def delete_supplier(session: Session, supplier_id: int) -> bool:
    supplier = session.query(Supplier).filter_by(id=supplier_id).first()
    if supplier:
        session.delete(supplier)
        return True
    return False
