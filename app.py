from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash

app = Flask(__name__)
CORS(app)

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
