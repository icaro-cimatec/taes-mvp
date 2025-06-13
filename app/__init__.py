from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)
    
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    from app.views.auth_view import auth_bp
    from app.views.product_view import product_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    with app.app_context():
        db.create_all()

    return app
