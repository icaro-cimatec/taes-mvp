from app import db
from app.models.comment import Comment


def add_comment(data):
    comment = Comment(
        product_id=data['product_id'],
        author=data['author'],
        content=data['content'],
        rating=data['rating']
    )
    db.session.add(comment)
    db.session.commit()
    return comment


def get_comments_by_product(product_id):
    return Comment.query.filter_by(product_id=product_id).all()
