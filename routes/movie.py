from flask import Blueprint, request, jsonify
from extensions import db
from models import Movie, Rating

movie_bp = Blueprint('movie', __name__, url_prefix='/api/movie')

@movie_bp.route('/rate', methods=['POST'])
def rate_movie():
    """给电影评分（需提供user_id和movie_id）"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['user_id', 'movie_id', 'score']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要字段'}), 400
    
    # 检查评分是否合法（0-5分）
    if not 0 <= float(data['score']) <= 5:
        return jsonify({'error': '评分需在0-5分之间'}), 400
    
    # 创建或更新评分
    rating = Rating.query.filter_by(
        user_id=data['user_id'],
        movie_id=data['movie_id']
    ).first()
    
    if rating:
        rating.score = data['score']  # 更新已有评分
    else:
        rating = Rating(
            user_id=data['user_id'],
            movie_id=data['movie_id'],
            score=data['score']
        )
        db.session.add(rating)
    
    db.session.commit()
    return jsonify({'message': 'sucess'}), 201
