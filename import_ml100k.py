#导入mobielens的数据

import pandas as pd
from models import app, db
from models import Movie, Rating
from datetime import datetime

def import_movies():
    """导入电影数据（对应MovieLens的u.item文件）"""
    # 读取数据（列分隔符为|，无表头，Latin1编码处理特殊字符）
    df = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin1', header=None)
    
    for _, row in df.iterrows():
        movie = Movie(
            id=row[0],  # 第一列为电影ID
            title=row[1],  # 第二列为标题
            genres='|'.join([  # 拼接类型标记为字符串
                genre for genre, flag in zip([
                    'Action', 'Adventure', 'Animation', 
                    'Children', 'Comedy', 'Crime'  # 完整列表见MovieLens数据说明
                ], row[5:24]) if flag == '1'
            ])
        )
        db.session.add(movie)
    db.session.commit()

def import_ratings():
    """导入评分数据（对应MovieLens的u.data文件）"""
    df = pd.read_csv('ml-100k/u.data', sep='\t', header=None, 
                    names=['user_id', 'movie_id', 'score', 'timestamp'])
    
    for _, row in df.iterrows():
        rating = Rating(
            user_id=row['user_id'],
            movie_id=row['movie_id'],
            score=row['score'],
            timestamp=datetime.fromtimestamp(row['timestamp'])  # 转换时间戳
        )
        db.session.add(rating)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        import_movies()
        import_ratings()
    print("MovieLens 100K数据集导入完成！")