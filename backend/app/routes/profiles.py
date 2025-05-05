from flask import Blueprint, request, jsonify
from app import db, jwt
from app.models import User, Profile, Favorite
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_profiles():
    print("ok")
    current_user_id = get_jwt_identity()
    print("No")
    user_profiles = Profile.query.filter_by(user_id_fk=current_user_id).first()
    if not user_profiles:
        return jsonify({'error': 'You must create a profile first.'}), 400
    profiles = Profile.query.options(joinedload(Profile.user)).order_by(Profile.created_at.desc()).limit(4).all()
    return jsonify([profile.to_dict(current_user_id=current_user_id) for profile in profiles]), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    print(data)
    if Profile.query.filter_by(user_id_fk=current_user_id).count() >= 3:
        return jsonify({'message': 'Maximum of 3 profiles per user reached'}), 400
    
    required_fields = [
        'description', 'parish', 'biography', 'sex', 'race', 'birth_year',
        'height', 'fav_cuisine', 'fav_colour', 'fav_school_subject',
        'political', 'religious', 'family_oriented'
    ]
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required profile fields'}), 400
    
    profile = Profile(
        user_id_fk=current_user_id,
        description=data['description'],
        parish=data['parish'],
        biography=data['biography'],
        sex=data['sex'],
        race=data['race'],
        birth_year=data['birth_year'],
        height=data['height'],
        fav_cuisine=data['fav_cuisine'],
        fav_colour=data['fav_colour'],
        fav_school_subject=data['fav_school_subject'],
        political=data['political'],
        religious=data['religious'],
        family_oriented=data['family_oriented']
    )
    
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({'message': 'Profile created successfully', 'profile_id': profile.id}), 201

@bp.route('/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify(profile.to_dict()), 200

@bp.route('/<int:user_id>/favourite', methods=['POST'])
@jwt_required()
def add_favorite(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id == user_id:
        return jsonify({'message': 'Cannot favorite yourself'}), 400
    
    if Favorite.query.filter_by(user_id_fk=current_user_id, fav_user_id_fk=user_id).first():
        return jsonify({'message': 'User already in favorites'}), 400
    
    favorite = Favorite(
        user_id_fk=current_user_id,
        fav_user_id_fk=user_id
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': 'User added to favorites'}), 201

@bp.route('/matches/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_matches(profile_id):
    current_user_id = get_jwt_identity()
    profile = Profile.query.get_or_404(profile_id)
    
    if profile.user_id_fk != current_user_id:
        return jsonify({'message': 'Not authorized to view matches for this profile'}), 403
    
    all_profiles = Profile.query.filter(Profile.user_id_fk != current_user_id).all()
    
    matches = []
    for p in all_profiles:
        age_diff = abs(profile.birth_year - p.birth_year)
        if age_diff > 5:
            continue
        
        height_diff = abs(profile.height - p.height)
        if height_diff < 3 or height_diff > 10:
            continue
        
        matched_fields = 0
        if profile.fav_cuisine == p.fav_cuisine:
            matched_fields += 1
        if profile.fav_colour == p.fav_colour:
            matched_fields += 1
        if profile.fav_school_subject == p.fav_school_subject:
            matched_fields += 1
        if profile.political == p.political:
            matched_fields += 1
        if profile.religious == p.religious:
            matched_fields += 1
        if profile.family_oriented == p.family_oriented:
            matched_fields += 1
            
        if matched_fields >= 3:
            matches.append(p.to_dict())
    
    return jsonify(matches), 200