from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = []

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
