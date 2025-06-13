import pytest
from flask import Flask
from app import db
from app.views.product_view import product_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.register_blueprint(product_bp)
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client


def test_add_product(client, monkeypatch):
    mock_product = type('Product', (), {'id': 1})()
    monkeypatch.setattr('app.views.product_view.create_product',
                        lambda data: mock_product)

    response = client.post('/api/products', json={
        'name': 'Produto Teste',
        'description': 'Descrição do produto teste',
        'price': 100.0,
        'artisan': 'Artisan Teste'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Produto cadastrado"
    assert data["id"] == 1


def test_get_products(client, monkeypatch):
    mock_products = [
        {'id': 1,
         'name': 'Produto 1',
         'description': 'Descrição 1',
         'price': 50.0,
         'artisan': 'Artisan 1'},

        {'id': 2,
         'name': 'Produto 2',
         'description': 'Descrição 2',
         'price': 75.0,
         'artisan': 'Artisan 2'}
    ]
    monkeypatch.setattr('app.views.product_view.get_products', lambda: mock_products)

    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Produto 1"
    assert data[1]["name"] == "Produto 2"
