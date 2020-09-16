from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from app.core import auth
from app.lists.models import List
from app.lists.schemas import ListSchema, ListItemSchema, PurchasedListItemSchema
from app.products.models import Product


lists_api = Blueprint('lists_api', __name__)


@lists_api.route('/', methods=['POST'])
@auth.login
def create_list(auth_user):
    data = request.get_json()
    schema = ListSchema()

    errors = schema.validate(data)
    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    load_data = schema.load(data)
    load_data['owner'] = auth_user
    list_obj = schema.create(load_data)
    return jsonify(schema.dump(list_obj)), HTTPStatus.CREATED


@lists_api.route('/', methods=['GET'])
@lists_api.route('/<int:list_id>/', methods=['GET'])
@auth.login
def retrieve_lists(auth_user, list_id=None):
    if list_id:
        list_obj = List.query.filter_by(id=list_id).first_or_404()
        return jsonify(ListSchema().dump(list_obj)), HTTPStatus.OK

    lists = List.query.all()
    return jsonify(ListSchema(many=True).dump(lists)), HTTPStatus.OK


@lists_api.route('/<int:list_id>/list-items/', methods=['POST'])
@auth.login
def create_list_items(auth_user, list_id=None):
    data = request.get_json()

    list_obj = List.query.filter_by(id=list_id).first_or_404()

    product_id = data.pop('product', None)
    product_obj = Product.query.filter_by(id=product_id).first()

    schema = ListItemSchema(context={
        'product_id': product_id,
        'list': list_obj
    })
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    load_data = schema.load(data)
    load_data['product'] = product_obj
    load_data['list'] = list_obj
    list_item_obj = schema.create(load_data)
    return jsonify(schema.dump(list_item_obj)), HTTPStatus.CREATED


@lists_api.route('/<int:list_id>/list-items/<int:list_item_id>/purchased/', methods=['POST'])
@auth.login
def purchased_list_items(auth_user, list_id, list_item_id):
    data = request.get_json(silent=True) or {}
    list_obj = List.query.filter_by(id=list_id).first_or_404()
    list_item_obj = list_obj.list_items.filter_by(id=list_item_id).first_or_404()

    context_data = {
        'purchased_by': auth_user,
        'list': list_obj,
        'list_item': list_item_obj,
    }
    schema = PurchasedListItemSchema(context=context_data)

    errors = schema.validate(data)
    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    data.update(context_data)
    purchased_list_item_obj = schema.create(data)
    return jsonify(schema.dump(purchased_list_item_obj)), HTTPStatus.CREATED
