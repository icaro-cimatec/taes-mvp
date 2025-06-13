from flask import Blueprint, request, jsonify

checkout_bp = Blueprint('checkout', __name__)


@checkout_bp.route('/api/checkout', methods=['POST'])
def fake_checkout():
    data = request.json
    return jsonify({'message': 'Checkout simulado com sucesso',
                    'itens': len(data.get('cart', []))})
