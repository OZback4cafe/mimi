from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models import Menu

menu_blp = Blueprint('Menus', 'menus', description='Operations on menus', url_prefix='/menu' )

# API LIST:
# (1) 전체 메뉴 데이터 조회(GET)
# (2) 메뉴 생성 (POST)
@menu_blp.route('/')
class MenuList(MethodView):
    def get(self):
        menus = Menu.query.all()

        menu_data = [
            {'id':menu.id, 
             'category_id':menu.category_id, 
             'name':menu.name, 
             'price':menu.price} 
             for menu in menus
        ]
         
        return jsonify(menu_data)
    
    def post(self):
        data = request.json

        new_menu =Menu(category_id=data['category_id'], name=data['name'], price=data['price'])
        db.session.add(new_menu)
        db.session.commit()

        return jsonify({'msg':'Successfully created new menu'}), 201

# (1) 특정 메뉴 데이터 조회 (GET)
# (2) 특정 메뉴 데이터 업데이트 (PUT)
# (3) 특정 메뉴 삭제 (DELETE)

@menu_blp.route("/<int:menu_id>")
class MenuResource(MethodView):
    def get(self, menu_id):
        menu = Menu.query.get_or_404(menu_id)

        return jsonify({'category_id':menu.category_id, 'name':menu.name, 'price':menu.price})
    
    def put(self, menu_id):
        menu = Menu.query.get_or_404(menu_id)
        data = request.json

        menu.category_id = data['category_id']
        menu.name = data['name']
        menu.price = data['price']

        db.session.commit()

        return jsonify({'msg':'Successfully updated menu'}), 200
    
    def delete(self, menu_id):
        menu = Menu.query.get_or_404(menu_id)
        
        db.session.delete(menu)
        db.session.commit()

        return jsonify({'msg':'Successfully delete menu'}), 204


        