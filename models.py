from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'  # 显式指定表名
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    ratings = db.relationship('Rating', backref='user', lazy=True)  # 修正backref名称

class Movie(db.Model):
    __tablename__ = 'movie'  # 显式指定表名
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    ratings = db.relationship('Rating', backref='movie', lazy=True)  # 修正backref名称

class Rating(db.Model):
    __tablename__ = 'rating'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'movie_id', name='uix_user_movie'),
    )
