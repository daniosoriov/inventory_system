from decorators import handle_exceptions
from models import Supplier, Product
from orm_setup import SessionLocal

session = SessionLocal()


# Supplier operations
@handle_exceptions
def create_supplier(name: str, email: str, phone_number: str) -> Supplier:
    with session.begin():
        new_supplier = Supplier(
            name=name,
            email=email,
            phone_number=phone_number
        )
        session.add(new_supplier)
        session.commit()
        return new_supplier


@handle_exceptions
def get_supplier(supplier_id: int) -> Supplier | None:
    with session.begin():
        supplier = session.query(Supplier).filter_by(id=supplier_id).first()
        return supplier


@handle_exceptions
def update_supplier(supplier_id: int, name: str = None, email: str = None, phone_number: str = None) -> Supplier | None:
    with session.begin():
        supplier = session.query(Supplier).filter_by(id=supplier_id).first()
        if supplier:
            if name:
                supplier.name = name
            if email:
                supplier.email = email
            if phone_number:
                supplier.phone_number = phone_number
            session.commit()
            return supplier
        return None


@handle_exceptions
def delete_supplier(supplier_id: int) -> bool:
    with session.begin():
        supplier = session.query(Supplier).filter_by(id=supplier_id).first()
        if supplier:
            session.delete(supplier)
            session.commit()
            return True
        return False


# Product operations
@handle_exceptions
def create_product(name: str, description: str, sku: str, price: float, supplier_id: int) -> Product:
    with session.begin():
        new_product = Product(
            name=name,
            description=description,
            sku=sku,
            price=price,
            supplier_id=supplier_id
        )
        session.add(new_product)
        session.commit()
        return new_product


@handle_exceptions
def get_product(product_id: int) -> Product | None:
    with session.begin():
        product = session.query(Product).filter_by(id=product_id).first()
        return product


@handle_exceptions
def update_product(product_id: int, name: str = None, description: str = None, sku: str = None,
                   price: float = None) -> Product | None:
    with session.begin():
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            if name:
                product.name = name
            if description:
                product.description = description
            if sku:
                product.sku = sku
            if price:
                product.price = price
            session.commit()
            return product
        return None


@handle_exceptions
def delete_product(product_id: int) -> bool:
    with session.begin():
        product = session.query(Product).filter_by(id=product_id).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False
