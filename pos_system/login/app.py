from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from db import Db
import models

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@127.0.0.1/back_cafe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
with app.app_context():
    db.create_all()
    # 기본 유저 존재 여부 확인
    admin_user = User.query.filter_by(username='admin').first()

    if not admin_user:
        # 기본 유저가 없으면 생성
        hashed_password = generate_password_hash('pw123', method='pbkdf2:sha256')
        new_user = User(username='admin', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print('기본 유저(admin)가 생성되었습니다.')


@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 데이터베이스에서 사용자 정보 가져오기
    user = User.query.filter_by(username=username).first()

    # 사용자 존재 여부와 비밀번호 일치 여부 확인
    if user and check_password_hash(user.password, password):
        # 로그인 성공 시 pos.html로 이동
        return jsonify({'success': True, 'message': '로그인 성공! POS로 이동합니다.'}), 200
    else:
        # 로그인 실패 시 에러 메시지 반환
        return jsonify({'success': False, 'message': '로그인 실패! 유효한 사용자 이름 또는 비밀번호가 아닙니다.'}), 401

@app.route('/pos/<username>', methods=['GET'])
def pos(username):
    
    return render_template('pos.html',username=username)





# 포인트 관리.........

Db.init_db()


@app.route('/point/<totalAmount>', methods=['GET'])
def point_system(totalAmount):
    return render_template('point_system.html',totalAmount=totalAmount)

@app.route('/api/get_customer_info', methods=['POST'])
def get_customer_info():
    data = request.get_json()
    phone = data.get('phone')
    
    connection = sqlite3.connect('cafe_order_system.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM customers WHERE phone_number = ?', (phone,))
    customer = cursor.fetchone()
    connection.close()

    if customer:
        response = {
            'success': True,
            'customer': {
                'name': customer[1],
                'birthday': customer[2],
                'points': customer[3]
            }
        }
    else:
        response = {'success': False}

    return jsonify(response)

@app.route('/new_customer')
def new_customer():
    phone = request.args.get('phone')
    return render_template('new_customer.html', phone=phone)

@app.route('/customer_info')
def customer_info():
    phone = request.args.get('phone')
    return render_template('customer_info.html', phone=phone)

@app.route('/api/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    phone = data.get('phone')
    name = data.get('name')
    birthday = data.get('birthday')

    connection = sqlite3.connect('cafe_order_system.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM customers WHERE phone_number = ?', (phone,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        # 고객이 이미 있는 경우 정보를 반환
        response = {
            'success': False,
            'exists': True,
            'customer': {
                'name': existing_customer[1],
                'birthday': existing_customer[2],
                'points': existing_customer[3]
            }
        }
    else:
        # 고객 등록
        try:
            cursor.execute('INSERT INTO customers (phone_number, name, birthday, points) VALUES (?, ?, ?, ?)', 
                           (phone, name, birthday, 0))
            connection.commit()
            response = {'success': True}
        except sqlite3.IntegrityError:
            response = {'success': False, 'exists': False}

    connection.close()
    
    return jsonify(response)

@app.route('/api/add_points', methods=['POST'])
def add_points():
    data = request.get_json()
    phone = data.get('phone')
    points_to_add = data.get('points', 0)

    connection = sqlite3.connect('cafe_order_system.db')
    cursor = connection.cursor()

    cursor.execute('SELECT points FROM customers WHERE phone_number = ?', (phone,))
    customer = cursor.fetchone()

    if customer:
        new_points = customer[0] + points_to_add
        cursor.execute('UPDATE customers SET points = ? WHERE phone_number = ?', (new_points, phone))
        connection.commit()
        response = {'success': True}
    else:
        response = {'success': False}

    connection.close()
    return jsonify(response)

@app.route('/api/edit_customer', methods=['POST'])
def edit_customer():
    data = request.get_json()
    phone = data.get('phone')
    name = data.get('name')
    birthday = data.get('birthday')

    connection = sqlite3.connect('cafe_order_system.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM customers WHERE phone_number = ?', (phone,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        cursor.execute('UPDATE customers SET name = ?, birthday = ? WHERE phone_number = ?', 
                       (name, birthday, phone))
        connection.commit()
        response = {'success': True}
    else:
        response = {'success': False}

    connection.close()
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
