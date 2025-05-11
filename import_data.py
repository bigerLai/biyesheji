import csv
from datetime import datetime
import pandas as pd
from app import app
from extensions import db
from models import Movie, Rating

def import_data():
    with app.app_context():
        # 清空旧数据
        db.session.query(Movie).delete()
        db.session.commit()

        # --- 1. 导入电影数据 ---
        try:
            # 读取完整列定义（u.item实际有24列）
            all_columns = ['id', 'title', 'release_date', 'video_release_date', 'imdb_url'] + \
                        ['unknown', 'action', 'adventure', 'animation', 'children', 
                         'comedy', 'crime', 'documentary', 'drama', 'fantasy', 
                         'film_noir', 'horror', 'musical', 'mystery', 'romance',
                         'sci_fi', 'thriller', 'war', 'western']
            
            movies = pd.read_csv(
                'data/u.item',
                sep='|',
                encoding='latin1',
                header=None,
                names=all_columns
            )
            
            # 数据类型转换
            movies['id'] = movies['id'].astype(int)
            movies['title'] = movies['title'].astype(str)
            
            # 处理genres：将19个类型列转换为管道分隔的字符串
            genre_columns = all_columns[5:]  # 第6列开始是类型
            movies['genres'] = movies[genre_columns].apply(
                lambda row: '|'.join([genre for genre, val in zip(genre_columns, row) if val == 1]),
                axis=1
            )

            # 单次插入
            for _, row in movies.iterrows():
                db.session.add(Movie(
                    id=int(row['id']),
                    title=str(row['title']),
                    genres=str(row['genres'])
                ))
                
            db.session.commit()
            print(f"✅ 电影数据导入成功！共 {len(movies)} 条记录")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ 电影数据导入失败: {str(e)}")

 # --- 2. 导入评分数据 ---
        try:
            ratings = pd.read_csv(
                'data/u.data',
                sep='\t',
                header=None,
                names=['user_id', 'movie_id', 'score', 'timestamp']
            )
            ratings['user_id'] = ratings['user_id'].astype(int)
            ratings['movie_id'] = ratings['movie_id'].astype(int)
            ratings['score'] = ratings['score'].astype(float)
            
            for _, row in ratings.iterrows():
                db.session.add(Rating(
                    user_id=int(row['user_id']),
                    movie_id=int(row['movie_id']),
                    score=float(row['score']),
                    timestamp=datetime.fromtimestamp(int(row['timestamp']))
                ))
            db.session.commit()
            print("✅ 评分数据导入成功！")
        except Exception as e:
            db.session.rollback()
            print(f"❌ 评分数据导入失败: {e}")

if __name__ == '__main__':
    import_data()
