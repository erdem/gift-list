from marshmallow import Schema, fields
from app.database import db
from app.lists.models import List
from app.products.schemas import ProductSchema
from app.users.schemas import UserSchema


class ListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    product = fields.Nested(ProductSchema, many=False)
    quantity = fields.Integer(required=True, default=1)
    created_at = fields.DateTime(dump_only=True)

    def create(self, data):
        pass


class ListSchema(Schema):
    id = fields.Integer(dump_only=True)
    owner = fields.Nested(UserSchema, many=False, dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)

    @classmethod
    def create(cls, data, **kwargs):
        list_obj = List(**data)
        db.session.add(list_obj)
        db.session.commit()
        return list_obj


class PurchasedListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    purchased_by = fields.Nested(UserSchema, many=False, required=True)
    list = fields.Nested(ListSchema, many=False, required=True)
    list_item = fields.Nested(ListItemSchema, many=False, required=True)
    created_at = fields.DateTime(dump_only=True)

    def create(self, data):
        pass
