from flask import Blueprint, request, jsonify
from app import db
from app.models import Profile, User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('search', __name__, url_prefix='/api/search')

@bp.route('/', methods=['GET'])
@jwt_required()
def search_profiles():
    current_user_id = get_jwt_identity()
    query = Profile.query.filter(Profile.user_id_fk != current_user_id)
    
    name = request.args.get('name')
    birth_year = request.args.get('birth_year')
    sex = request.args.get('sex')
    race = request.args.get('race')
    
    if name:
        query = query.join(User).filter(User.name.ilike(f'%{name}%'))
    if birth_year:
        query = query.filter(Profile.birth_year == birth_year)
    if sex:
        query = query.filter(Profile.sex == sex)
    if race:
        query = query.filter(Profile.race == race)
    
    profiles = query.all()
    return jsonify([profile.to_dict() for profile in profiles]), 200