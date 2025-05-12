# app.py
from flask import Flask
from extensions import db  # 从extensions导入db
from config import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\project\\lunwen\\instance\\app.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(config['development'])  # 自动加载配置


# 🔐 生产环境必须添加（放在这里！）
app.config['SECRET_KEY'] = 'your-random-secret-key'  # 实际使用时应替换为随机字符串

# 关键步骤：绑定app到db，并导入模型
db.init_app(app)

# 新增：导入并注册蓝图
from routes.user import user_bp
from routes.movie import movie_bp
app.register_blueprint(user_bp)
app.register_blueprint(movie_bp)

 
# 保留原有路由
@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__main__': 
    app.run()  # 删除debug=True参数
