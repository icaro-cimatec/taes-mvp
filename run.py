from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.config.from_object(Config)

    db.init_app(app)

    app.run(debug=True)
