import argparse
import logging.config

from orm_setup import SessionLocal
from models import OperationType
from crud.supplier import create_supplier, get_supplier, update_supplier, delete_supplier
from crud.product import create_product, get_product, update_product, delete_product, update_stock

from logger import LOGGING_CONF

logging.config.dictConfig(LOGGING_CONF)
logger = logging.getLogger(__name__)

session = SessionLocal()


def setup_parser():
    parser = argparse.ArgumentParser(description="CLI for managing suppliers and products.")
    subparsers = parser.add_subparsers(dest='command')

    # Add subcommands for supplier
    create_supplier_parser = subparsers.add_parser('create_supplier', help='Create a new supplier')
    create_supplier_parser.add_argument('--name', required=True, help='Name of the supplier')
    create_supplier_parser.add_argument('--email', required=True, help='Email of the supplier')
    create_supplier_parser.add_argument('--phone_number', required=True, help='Phone number of the supplier')

    get_supplier_parser = subparsers.add_parser('get_supplier', help='Get a supplier by ID')
    get_supplier_parser.add_argument('--id', required=True, type=int, help='ID of the supplier to retrieve')

    update_supplier_parser = subparsers.add_parser('update_supplier', help='Update an existing supplier')
    update_supplier_parser.add_argument('--id', required=True, type=int, help='ID of the supplier to update')
    update_supplier_parser.add_argument('--name', help='New name of the supplier')
    update_supplier_parser.add_argument('--email', help='New email of the supplier')
    update_supplier_parser.add_argument('--phone_number', help='New phone number of the supplier')

    delete_supplier_parser = subparsers.add_parser('delete_supplier', help='Delete a supplier')
    delete_supplier_parser.add_argument('--id', required=True, type=int, help='ID of the supplier to delete')

    # Add subcommands for products
    create_product_parser = subparsers.add_parser('create_product', help='Create a new product')
    create_product_parser.add_argument('--name', required=True, help='Name of the product')
    create_product_parser.add_argument('--description', help='Description of the product')
    create_product_parser.add_argument('--sku', required=True, help='SKU of the product')
    create_product_parser.add_argument('--price', required=True, type=float, help='Price of the product')
    create_product_parser.add_argument('--supplier_id', required=True, type=int, help='ID of the supplier')
    create_product_parser.add_argument('--stock', required=True, type=int, help='Stock of the product', default=0)

    get_product_parser = subparsers.add_parser('get_product', help='Get a product by ID')
    get_product_parser.add_argument('--id', required=True, type=int, help='ID of the product to retrieve')

    update_product_parser = subparsers.add_parser('update_product', help='Update an existing product')
    update_product_parser.add_argument('--id', required=True, type=int, help='ID of the product to update')
    update_product_parser.add_argument('--name', help='New name of the product')
    update_product_parser.add_argument('--description', help='New description of the product')
    update_product_parser.add_argument('--sku', help='New SKU of the product')
    update_product_parser.add_argument('--price', type=float, help='New price of the product')

    delete_product_parser = subparsers.add_parser('delete_product', help='Delete a product')
    delete_product_parser.add_argument('--id', required=True, type=int, help='ID of the product to delete')

    # Add subcommands for stock operations
    update_stock_parser = subparsers.add_parser('update_stock', help='Update stock for a product')
    update_stock_parser.add_argument('--product_id', required=True, type=int, help='ID of the product')
    update_stock_parser.add_argument('--quantity', required=True, type=int, help='Quantity to add or remove')
    update_stock_parser.add_argument('--operation', required=True, choices=[op.name for op in OperationType], )

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    log_messages = []
    with session.begin():
        if args.command == 'create_supplier':
            supplier = create_supplier(session, args.name, args.email, args.phone_number)
            session.flush()
            log_messages.append(f"Created new supplier {supplier}")

        elif args.command == 'get_supplier':
            supplier = get_supplier(session, args.id)
            if supplier:
                log_messages.append(f"Retrieved supplier: {supplier}")
            else:
                log_messages.append(f"Supplier with ID {args.id} not found")

        elif args.command == 'update_supplier':
            supplier = update_supplier(session, args.id, args.name, args.email, args.phone_number)
            if supplier:
                session.flush()
                log_messages.append(f"Updated supplier {supplier}")
            else:
                log_messages.append(f"Supplier with ID {args.id} not found")

        elif args.command == 'delete_supplier':
            deleted = delete_supplier(session, args.id)
            if deleted:
                log_messages.append(f"Deleted supplier with ID {args.id}")
            else:
                log_messages.append(f"Supplier with ID {args.id} not found")

        elif args.command == 'create_product':
            product = create_product(session, args.name, args.description, args.sku, args.price, args.supplier_id)
            session.flush()
            log_messages.append(f"Created new product {product.id}")
            update_stock(session, product.id, args.stock, OperationType.ADD)
            log_messages.append(f"Updated stock for product {product.id} to {args.stock}")

        elif args.command == 'get_product':
            product = get_product(session, args.id)
            if product:
                log_messages.append(f"Retrieved product {product}")
            else:
                log_messages.append(f"Product with ID {args.id} not found")

        elif args.command == 'update_product':
            product = update_product(session, args.id, args.name, args.description, args.sku, args.price)
            if product:
                session.flush()
                log_messages.append(f"Updated product {product}")
            else:
                log_messages.append(f"Product with ID {args.id} not found")

        elif args.command == 'delete_product':
            deleted = delete_product(session, args.id)
            if deleted:
                log_messages.append(f"Deleted product with ID {args.id}")
            else:
                log_messages.append(f"Product with ID {args.id} not found")

        elif args.command == 'update_stock':
            updated = update_stock(session, args.product_id, args.quantity, OperationType[args.operation])
            if updated:
                log_messages.append(f"Updated stock for product {args.product_id}")
            else:
                log_messages.append(f"Not possible to update stock for product {args.product_id}")

    for message in log_messages:
        logger.info(message)


if __name__ == '__main__':
    main()
