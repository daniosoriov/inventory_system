from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Supplier(Base):
    """
    Represents a supplier that provides products.

    This class models a supplier entity in the system, holding information about
    the supplier's name, email, contact details, and the products they provide.
    The supplier can be associated with multiple products, which are handled using
    a relationship with the `Product` class.

    :ivar id: The identifier of the supplier, serves as the primary key.
    :type id: int
    :ivar name: Name of the supplier.
    :type name: str
    :ivar email: Email address of the supplier.
    :type email: str
    :ivar phone_number: The contact phone number of the supplier.
    :type phone_number: str
    :ivar products: A list of products associated with the supplier.
    Deleting a supplier will also delete orphans in the `Product` association.
    :type products: List['Product']
    """
    __tablename__ = 'supplier'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[List['Product']] = relationship(
        'Product',
        back_populates='supplier',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Supplier(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone_number={self.phone_number!r})>"


class Product(Base):
    """
    Represents a product entity in the application.

    This class defines the structure and attributes of a product entity, including its
    relationships to other entities.
    It includes details such as the product name,
    description, stock-keeping unit (SKU), price, and associated supplier.

    :ivar id: Unique identifier of the product.
    :type id: int
    :ivar name: Name of the product. This is a required field and must not exceed 50 characters.
    :type name: str
    :ivar description: A detailed description of the product. This field is optional and allows up to 200 characters.
    :type description: str
    :ivar sku: Stock-keeping unit of the product. This is a required and unique field, indexed for optimization.
    :type sku: str
    :ivar price: The price of the product. Must be specified and cannot be null.
    :type price: float
    :ivar supplier_id: Identifier of the supplier associated with the product.
    :type supplier_id: int
    :ivar supplier: Relationship to the Supplier entity representing the supplier of the product.
    :type supplier: Supplier
    """
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    sku: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    price: Mapped[float] = mapped_column(nullable=False)
    supplier_id: Mapped[int] = mapped_column(ForeignKey('supplier.id'))

    supplier: Mapped['Supplier'] = relationship(back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id!r}, name={self.name!r}, description={self.description!r}, sku={self.sku!r}, price={self.price!r}, supplier_id={self.supplier_id!r})>"
