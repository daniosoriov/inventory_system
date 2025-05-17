from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Supplier(Base):
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
