from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from app.lists.models import List
from app.lists.schemas import ListSchema

lists_api = Blueprint('lists_api', __name__)


@lists_api.route('/', methods=["POST"])
def create_list():
    data = request.get_json()
    schema = ListSchema()

    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST
    return jsonify(schema.dump(schema.instance)), HTTPStatus.CREATED


@lists_api.route('/', methods=["GET"])
@lists_api.route('/<int:list_id>/', methods=["GET"])
def retrieve_list(list_id=None):
    if list_id:
        list_obj = List.query.filter_by(id=list_id).first_or_404()
        return jsonify( ListSchema().dump(list_obj)), HTTPStatus.OK

    lists = List.query.all()
    return jsonify(ListSchema(many=True).dump(lists)), HTTPStatus.OK

