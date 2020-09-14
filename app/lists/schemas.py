from marshmallow import Schema, fields, validates, ValidationError, post_load, validates_schema

from app.database import db
from app.lists.models import List
from app.products.schemas import ProductSchema
from app.users.models import User
from app.users.schemas import UserSchema


class ListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    product = fields.Nested(ProductSchema, many=False)
    quantity = fields.Integer(required=True, default=1)
    created_at = fields.DateTime(dump_only=True)


class ListSchema(Schema):
    id = fields.Integer(dump_only=True)
    owner = fields.Nested(UserSchema, many=False, required=True)
    name = fields.String(required=True)
    status = fields.Method("get_list_Item_status")
    created_at = fields.DateTime(dump_only=True)

    def get_list_item_status(self, list_item):
        pass

    @validates_schema()
    def validate_owner_id(self, data, **kwargs):
        try:
            owner_id = int(data['owner'])
        except (IndexError, ValueError):
            raise ValidationError('Invalid "owner" identifier value', field_name='owner')

        is_owner_id_valid = bool(
            User.query.filter_by(id=owner_id).first()
        )

        if not is_owner_id_valid:
            raise ValidationError('Owner does not exists', field_name='owner')

    @property
    def instance(self):
        """
        Returns created db entity object after `Schema` loaded.
        """
        try:
            return self._instance
        except AttributeError:
            raise AttributeError(f'"instance" attribute not accessible, you must loaded the schema to access.')

    @post_load
    def create_product(self, data, **kwargs):
        list_obj = List(**data)
        db.session.add(list_obj)
        db.session.commit()
        self._instance = list_obj


class PurchasedListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    purchased_by = fields.Nested(UserSchema, many=False, required=True)
    list = fields.Nested(ListSchema, many=False, required=True)
    list_item = fields.Nested(ListItemSchema, many=False, required=True)
    created_at = fields.DateTime(dump_only=True)


