# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')  # 生产环境务必修改！
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/app.db')
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/mydb')  # 示例PostgreSQL
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
