from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import create_user, get_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user = create_user(data)
    return jsonify({'message': 'Usuário cadastrado com sucesso', 'email': user.email}), 201

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    token = get_user(data)
    if not token:
        return jsonify({'error':'Credenciais inválidas'}), 401
    else:
        return jsonify({'token': token}), 201
