import pytest
from flask import Flask
from app import db
from app.views.comment_view import comment_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    app.register_blueprint(comment_bp)
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client


def test_create_comment_success(client, monkeypatch):
    # Mock do controller para simular criação do comentário
    mock_comment = type('Comment', (), {'id': 1})()
    monkeypatch.setattr('app.views.comment_view.add_comment', lambda data: mock_comment)

    response = client.post('/api/comments', json={
        'product_id': 1,
        'author': 'João',
        'content': 'Ótimo produto!',
        'rating': 5
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'Comentário adicionado' in data['message']
    assert data['id'] == 1


def test_get_comments_by_product(client, monkeypatch):
    # Mock da função que retorna comentários do produto
    mock_result = [
        type('Comment', (), {'author': 'Maria', 'content': 'Lindo', 'rating': 5})(),
        type('Comment', (), {'author': 'Lucas', 'content': 'Bom custo-benefício',
                             'rating': 4})()
    ]
    monkeypatch.setattr('app.views.comment_view.get_comments_by_product',
                        lambda pid: mock_result)

    response = client.get('/api/comments/1')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['author'] == 'Maria'
    assert data[1]['rating'] == 4
