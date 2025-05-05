from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    photo = db.Column(db.String(200))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    profiles = db.relationship('Profile', backref='user', lazy='dynamic')
    favorites = db.relationship('Favorite', foreign_keys='Favorite.user_id_fk', backref='user', lazy='dynamic')
    favorited_by = db.relationship('Favorite', foreign_keys='Favorite.fav_user_id_fk', backref='fav_user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'photo': self.photo,
            'date_joined': self.date_joined.isoformat() if self.date_joined else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    parish = db.Column(db.String(100), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    fav_cuisine = db.Column(db.String(100), nullable=False)
    fav_colour = db.Column(db.String(50), nullable=False)
    fav_school_subject = db.Column(db.String(100), nullable=False)
    political = db.Column(db.Boolean, nullable=False)
    religious = db.Column(db.Boolean, nullable=False)
    family_oriented = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, current_user_id=None):
        is_favorited = False
        if current_user_id:
            is_favorited = Favorite.query.filter_by(
                user_id_fk=current_user_id,
                fav_user_id_fk=self.user_id_fk
            ).first() is not None

        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'user_id': self.user_id_fk,
            'description': self.description,
            'parish': self.parish,
            'biography': self.biography,
            'sex': self.sex,
            'race': self.race,
            'birth_year': self.birth_year,
            'height': self.height,
            'fav_cuisine': self.fav_cuisine,
            'fav_colour': self.fav_colour,
            'fav_school_subject': self.fav_school_subject,
            'political': self.political,
            'religious': self.religious,
            'family_oriented': self.family_oriented,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_favorited': is_favorited
        }

    
    def __repr__(self):
        return f'<Profile {self.id} for User {self.user_id_fk}>'

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id_fk', 'fav_user_id_fk', name='unique_favorite'),
    )
    
    def __repr__(self):
        return f'<Favorite {self.user_id_fk} -> {self.fav_user_id_fk}>'