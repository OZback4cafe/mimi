from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from db import db
from models import Category

category_blp = Blueprint('categories', 'categories', description='Operations on categories', url_prefix='/category')

# API List
# /caregory/
# 전체 카테고리를 가져오는 API (GET)
# 카테고리 작성하는 API (POST)
@category_blp.route('/')
class CategoryList(MethodView):
    def get(self):
        categories = Category.query.all()

        return jsonify([{"id":category.id, 
                         'name':category.name} 

                         for category in categories])
  

    def post(self):
        data = request.json
        new_category= Category(id=data['id'], name=data['name'])
        db.session.add(new_category)
        db.session.commit()

        return jsonify({'msg': 'successfully created category'}), 200
    
# /category/<int: category_id>
# 하나의 카테고리 불러오기 (GET)
# 특정 카테고리 수정하기 (PUT)
# 특정 카테고리 삭제하기 (DELETE)
@category_blp.route("/<int:category_id>")
class CategoryResource(MethodView):
    def get(self, category_id):
        category = Category.query.get_or_404(category_id)

        return jsonify({'id': category.id,
                        'name': category.name,
                        })

    def put(self, category_id):
        category = Category.query.get_or_404(category_id)

        data = request.json

        category.name = data['name']

        db.session.commit()

        return jsonify({'msg': 'Successfully updated category data'}), 201

    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()

        return jsonify({"msg":"Successfully delete category data"}), 204
