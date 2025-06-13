from flask import Blueprint, request, jsonify
from app.controllers.product_controller import create_product

product_bp = Blueprint('product', __name__)

@product_bp.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    product = create_product(data)
    return jsonify({'message': 'Produto cadastrado', 'id': product.id})
