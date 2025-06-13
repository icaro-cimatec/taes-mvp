from flask import Blueprint, request, jsonify
from app.controllers.comment_controller import add_comment, get_comments_by_product

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/api/comments', methods=['POST'])
def create_comment():
    comment = add_comment(request.json)
    return jsonify({'message': 'Comentário adicionado', 'id': comment.id})


@comment_bp.route('/api/comments/<int:product_id>')
def list_comments(product_id):
    comments = get_comments_by_product(product_id)
    return jsonify([
        {'author': c.author, 'content': c.content, 'rating': c.rating} for c in comments
    ])
