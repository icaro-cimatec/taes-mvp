from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user = create_user(data)
    return jsonify({'message': 'Usuário cadastrado com sucesso', 'email': user.email})
