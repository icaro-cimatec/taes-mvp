from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'segredo_devsecops'

users = []
products = []

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2')
    users.append({
        'name': data['name'],
        'bio': data['bio'],
        'email': data['email'],
        'password': hashed_password
    })
    return jsonify({ 'message': 'Artesão cadastrado com sucesso' }), 201

# Rota de login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = next((u for u in users if u['email'] == data['email']), None)
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({ 'error': 'Credenciais inválidas' }), 401
    token = jwt.encode({
        'email': user['email'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({ 'token': token })

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    products.append({
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'artisan': data['artisan']
    })
    return jsonify({ 'message': 'Produto cadastrado com sucesso' }), 201


@app.route('/api/products', methods=['GET'])
def list_products():
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
