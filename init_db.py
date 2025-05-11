# init_db.py
from app import app
from extensions import db
from models import User, Movie, Rating

def init_database():
    with app.app_context():
        db.create_all()
        print("✅ 数据库表已创建！位置：instance/app.db")

if __name__ == '__main__':
    init_database()
