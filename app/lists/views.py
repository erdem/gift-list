from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from app.lists.models import List
from app.lists.schemas import ListSchema, ListItemSchema
from app.products.models import Product
from app.users.models import User


lists_api = Blueprint('lists_api', __name__)


@lists_api.route('/', methods=["POST"])
def create_list():
    data = request.get_json()
    schema = ListSchema()

    owner_id = data.pop('owner', None)
    owner = User.query.filter_by(id=owner_id).first()
    if not owner:
        return jsonify(
            {'owner': 'Invalid "owner" identifier value'}
        ), HTTPStatus.BAD_REQUEST

    errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    load_data = schema.load(data)
    load_data['owner'] = owner
    list_obj = schema.create(load_data)
    return jsonify(schema.dump(list_obj)), HTTPStatus.CREATED


@lists_api.route('/', methods=["GET"])
@lists_api.route('/<int:list_id>/', methods=["GET"])
def retrieve_lists(list_id=None):
    if list_id:
        list_obj = List.query.filter_by(id=list_id).first_or_404()
        return jsonify(ListSchema().dump(list_obj)), HTTPStatus.OK

    lists = List.query.all()
    return jsonify(ListSchema(many=True).dump(lists)), HTTPStatus.OK


@lists_api.route('/<int:list_id>/add-items/', methods=["GET"])
def add_list_items(list_id=None):
    data = request.get_json()

    list_obj = List.query.filter_by(id=list_id).first_or_404()

    product_id = data.pop('product', None)
    product_obj = Product.query.filter_by(id=product_id).first()

    validation_errors = {}
    if not product_obj:
        validation_errors['product'] = 'Invalid "product" identifier value'

    schema = ListItemSchema(context={
        'product': product_obj,
        'list': list_obj
    })
    errors = schema.validate(data)
    errors.update(validation_errors)
    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    load_data = schema.load(data)
    load_data['product'] = product_obj
    load_data['list'] = list_obj
    list_item_obj = schema.create(load_data)
    return jsonify(schema.dump(list_item_obj)), HTTPStatus.CREATED
