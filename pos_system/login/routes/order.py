from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models import Order

order_blp = Blueprint('Orders', 'orders', description='Operations on orders', url_prefix='/order' )

# API LIST:
# (1) 전체 주문 데이터 조회(GET)
# (2) 주문 생성 (POST)
@order_blp.route('/')
class OrderList(MethodView):
    def get(self):
        orders = Order.query.all()

        order_data = [
            {'id':order.id, 
             'nickname':order.nickname, 
             'points':order.points, 
             'menu_id':order.menu_id} 
             for order in orders
        ]
         
        return jsonify(order_data)
    
    def post(self):
        data = request.json

        new_order =Order(nickname=data['nickname'], points=data['points'], menu_id=data['menu_id'])
        db.session.add(new_order)
        db.session.commit()

        return jsonify({"msg":"Successfully created new order"}), 201

# (1) 특정 주문 데이터 조회 (GET)
# (2) 특정 주문 데이터 업데이트 (PUT)
# (3) 특정 주문 삭제 (DELETE)

@order_blp.route("/<int:order_id>")
class OrderResource(MethodView):
    def get(self, order_id):
        order = Order.query.get_or_404(order_id)

        return jsonify({'nickname':order.nickname, 'points':order.points, 'menu_id':order.menu_id})
    
    def put(self, order_id):
        order = Order.query.get_or_404(order_id)
        data = request.json

        order.nickname = data['nickname']
        order.points = data['points']
        order.menu_id = data['menu_id']

        db.session.commit()

        return jsonify({"msg": "Successfully updated order"}), 200
    
    def delete(self, order_id):
        order = Order.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()

        return jsonify({"msg": "Successfully delete order"}), 204
