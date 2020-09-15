from http import HTTPStatus

from flask import Blueprint, jsonify, request

from app.core import auth
from app.products.models import Product
from app.products.schemas import ProductSchema


products_api = Blueprint('products_api', __name__)


@products_api.route('/', methods=['POST'])
@auth.login
def create_products():
    data = request.get_json()
    schema = ProductSchema()

    errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST
    load_data = schema.load(data)
    product_obj = schema.create(load_data)
    return jsonify(schema.dump(product_obj)), HTTPStatus.CREATED


@products_api.route('/', methods=['GET'])
@products_api.route('/<int:product_id>/', methods=['GET'])
@auth.login
def retrieve_products(product_id=None):
    if product_id:
        product = Product.query.filter_by(id=product_id).first_or_404()
        return jsonify(ProductSchema().dump(product)), HTTPStatus.OK

    products = Product.query.all()
    return jsonify(ProductSchema(many=True).dump(products)), HTTPStatus.OK
