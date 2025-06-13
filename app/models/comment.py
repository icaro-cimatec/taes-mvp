from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    author = db.Column(db.String(100))
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)
