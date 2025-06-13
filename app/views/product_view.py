from flask import Blueprint, request, jsonify
from app.controllers.product_controller import create_product
from app.controllers.product_controller import get_products as get_products_controller
product_bp = Blueprint('product', __name__)


@product_bp.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    product = create_product(data)
    return jsonify({'message': 'Produto cadastrado', 'id': product.id}), 201


@product_bp.route('/api/products', methods=['GET'])
def get_products():
    products = get_products_controller()
    return jsonify(products), 200
