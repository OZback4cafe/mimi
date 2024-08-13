from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


import sqlite3

class Db:
    def init_db():
        connection = sqlite3.connect('cafe_order_system.db')
        cursor = connection.cursor()
        
        # 고객 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                phone_number TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                birthday TEXT NOT NULL,
                points INTEGER DEFAULT 0
            )
        ''')
        
        # 샘플 데이터 삽입 (이미 있는 경우 무시)
        cursor.execute('''
            INSERT OR IGNORE INTO customers (phone_number, name, birthday, points) 
            VALUES 
            ('01012345678', '홍길동', '1990-01-01', 150),
            ('01087654321', '이몽룡', '1992-02-15', 200)
        ''')
        
        connection.commit()
        connection.close()

    init_db()
