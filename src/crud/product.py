import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from decorators import handle_exceptions
from models import Product, ProductTransaction, OperationType

logger = logging.getLogger()


# Product operations
@handle_exceptions()
def create_product(session: Session,
                   name: str,
                   description: str,
                   sku: str,
                   price: float,
                   stock: int,
                   supplier_id: int) -> Product | None:
    try:
        new_product = Product(
            name=name,
            description=description,
            sku=sku,
            price=price,
            stock=stock,
            supplier_id=supplier_id,
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    except IntegrityError:
        session.rollback()
        raise ValueError(f"Product with SKU {sku} already exists.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating product: {e}")
        raise ValueError("An error occurred while creating the product.")


@handle_exceptions()
def get_product(session: Session, product_id: int) -> Product | None:
    product = session.query(Product).filter_by(id=product_id).first()
    return product


@handle_exceptions()
def update_product(session: Session, product_id: int, name: str = None, description: str = None, sku: str = None,
                   price: float = None) -> Product | None:
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        return None

    if name:
        product.name = name
    if description:
        product.description = description
    if sku:
        product.sku = sku
    if price:
        product.price = price
    return product


@handle_exceptions()
def delete_product(session: Session, product_id: int) -> bool:
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        session.delete(product)
        return True
    return False


# Transaction operations
def _create_transaction(session: Session, product_id: int, operation: OperationType,
                        quantity: int) -> ProductTransaction:
    new_transaction = ProductTransaction(
        product_id=product_id,
        operation=operation,
        quantity=quantity
    )
    session.add(new_transaction)
    return new_transaction


@handle_exceptions()
def get_transaction(session: Session, transaction_id: int) -> ProductTransaction | None:
    transaction = session.query(ProductTransaction).filter_by(id=transaction_id).first()
    return transaction


@handle_exceptions()
def update_stock(
        session: Session,
        product_id: int,
        quantity: int,
        operation: OperationType) -> bool:
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        message = f'Product {product_id} not found'
        logger.warning(message)
        raise ValueError(message)

    if operation in [OperationType.SUBTRACT, OperationType.SALE] and product.stock < quantity:
        message = f'Not enough stock for product {product_id}. Available: {product.stock}, Requested: {quantity}'
        logger.error(message)
        raise ValueError(message)

    product.stock += quantity if operation == OperationType.ADD else -quantity
    _create_transaction(session, product_id, operation=operation, quantity=quantity)
    return True
