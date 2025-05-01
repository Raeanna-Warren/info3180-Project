from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Profile, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@bp.route('/<int:user_id>/favourites', methods=['GET'])
@jwt_required()
def get_user_favorites(user_id):
    current_user_id = get_jwt_identity()
    
    if user_id != current_user_id:
        return jsonify({'message': 'Not authorized to view these favorites'}), 403
    
    favorites = Favorite.query.filter_by(user_id_fk=user_id).all()
    fav_users = [fav.fav_user.to_dict() for fav in favorites]
    
    return jsonify(fav_users), 200

@bp.route('/favourites/<int:n>', methods=['GET'])
def get_top_favorites(n):
    if n <= 0:
        return jsonify({'message': 'N must be a positive integer'}), 400
    
    top_users = db.session.query(
        User,
        db.func.count(Favorite.id).label('favorite_count')
    ).join(
        Favorite, User.id == Favorite.fav_user_id_fk
    ).group_by(
        User.id
    ).order_by(
        db.desc('favorite_count')
    ).limit(n).all()
    
    result = []
    for user, count in top_users:
        user_dict = user.to_dict()
        user_dict['favorite_count'] = count
        result.append(user_dict)
    
    return jsonify(result), 200