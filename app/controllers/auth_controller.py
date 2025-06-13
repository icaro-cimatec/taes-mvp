from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from app import db
from app.models.user import User
from app.config import Config

def create_user(data):
    user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_user(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return None

    token = jwt.encode({
        'email': user.email,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    }, Config.SECRET_KEY, algorithm='HS256')

    return token
