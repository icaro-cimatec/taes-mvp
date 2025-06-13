from app import db
from app.models.product import Product

def create_product(data):
    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        artisan_email=data['artisan']
    )
    db.session.add(product)
    db.session.commit()
    return product

def get_products():
    products = Product.query.all()
    return [product.to_dict() for product in products]
