from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/register', methods=['POST'])
def register():
    """用户注册（密码自动哈希）"""
    data = request.get_json()
    
    # 简单验证
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': '用户名和密码必填'}), 400
    
    # 检查用户名是否存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 409
    
    # 创建用户
    new_user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password'])  # 密码哈希化
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': '注册成功', 'user_id': new_user.id}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录（返回用户ID）"""
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'user_id': user.id, 'message': '登录成功'})
    
    return jsonify({'error': '用户名或密码错误'}), 401
