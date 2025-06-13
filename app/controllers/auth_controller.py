from werkzeug.security import generate_password_hash
from app import db
from app.models.user import User

def create_user(data):
    user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return user
