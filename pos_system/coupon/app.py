from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_mysqldb import MySQL
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'back_cafe'
mysql = MySQL(app)

# 이미지 업로드 설정
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 관리자 계정 정보
admin_credentials = {'username': 'admin', 'password': 'pw1234'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['logged_in'] = True
            return redirect(url_for('coupon_list'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/coupons')
def coupon_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM coupons")
    coupons = cur.fetchall()
    cur.close()
    return render_template('coupon_list.html', coupons=coupons)

@app.route('/coupon', methods=['GET', 'POST'])
def coupon_form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        coupon_id = request.form.get('coupon_id')
        cafe_name = request.form.get('cafe_name')
        coupon_name = request.form.get('coupon_name')
        if coupon_name == '직접 입력':
            coupon_name = request.form.get('coupon_name_input')
        barcode = str(uuid.uuid4())
        exchange_place = request.form['exchange_place']
        expiry_date = request.form['expiry_date']
        
        image = request.files['image']
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        cur = mysql.connection.cursor()
        if coupon_id:
            cur.execute("""
                UPDATE coupons 
                SET cafe_name=%s, coupon_name=%s, barcode=%s, exchange_place=%s, expiry_date=%s, image=%s 
                WHERE id=%s
            """, (cafe_name, coupon_name, barcode, exchange_place, expiry_date, image_filename, coupon_id))
        else:
            cur.execute("""
                INSERT INTO coupons (cafe_name, coupon_name, barcode, exchange_place, expiry_date, image) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cafe_name, coupon_name, barcode, exchange_place, expiry_date, image_filename))
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('coupon_list'))

    coupon_id = request.args.get('id')
    coupon = None
    if coupon_id:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM coupons WHERE id = %s", [coupon_id])
        coupon = cur.fetchone()
        cur.close()
    
    return render_template('coupon_form.html', coupon=coupon)

@app.route('/delete_coupon/<int:id>')
def delete_coupon(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM coupons WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('coupon_list'))

if __name__ == '__main__':
    app.run(debug=True)
