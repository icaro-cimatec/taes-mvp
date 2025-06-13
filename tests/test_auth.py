import pytest
from flask import Flask
from app import db
from app.views.auth_view import auth_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.register_blueprint(auth_bp)
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client


def test_register_success(client, monkeypatch):
    mock_user = type('User', (), {'email': 'test@example.com'})()
    monkeypatch.setattr('app.views.auth_view.create_user', lambda data: mock_user)
    response = client.post('/api/register', json={'name': 'test',
                                                  'email': 'test@example.com',
                                                  'password': '123456'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Usuário cadastrado com sucesso'
    assert data['email'] == 'test@example.com'


def test_login_success(client, monkeypatch):
    mock_token = "fake-jwt-token"
    monkeypatch.setattr('app.views.auth_view.get_user', lambda data: mock_token)
    response = client.get('/api/login', json={'email': 'test@example.com',
                                              'password': '123456'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['token'] == mock_token
