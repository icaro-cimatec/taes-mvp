from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'segredo_devsecops'
app.config['SECRET_KEY'] = 'segredo_devsecops'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artesaos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    artisan_email = db.Column(db.String(100))

with app.app_context():
    db.create_all()

users = []
products = []

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({ 'error': 'Email já cadastrado' }), 400
    hashed_password = generate_password_hash(data['password'], method='pbkdf2')
    new_user = User(name=data['name'], bio=data['bio'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({ 'message': 'Artesão cadastrado com sucesso' }), 201

# Rota de login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({ 'error': 'Credenciais inválidas' }), 401
    token = jwt.encode({
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({ 'token': token })

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        artisan_email=data['artisan']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({ 'message': 'Produto cadastrado com sucesso' }), 201

@app.route('/api/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    result = []
    for p in products:
        result.append({
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'artisan': p.artisan_email
        })
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
