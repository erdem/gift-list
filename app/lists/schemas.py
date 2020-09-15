from marshmallow import Schema, fields, validates_schema, ValidationError
from app.database import db
from app.lists.models import List, ListItem, PurchasedListItem
from app.products.schemas import ProductSchema
from app.users.schemas import UserSchema


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


class ListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    list = fields.Nested(ListSchema, many=False, dump_only=True)
    product = fields.Nested(ProductSchema, many=False)
    quantity = fields.Integer(required=True, default=1)
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def check_product_stock(self, data, **kwargs):
        product_obj = self.context.get('product')
        if not product_obj:
            raise ValidationError('Invalid product.')

        list_item_quantity = data.get('quantity')
        if not product_obj.in_stock_quantity >= list_item_quantity:
            raise ValidationError(f'"{product_obj.name}" is out of stock.')

    @classmethod
    def create(cls, data, **kwargs):
        list_item_obj = ListItem(**data)
        db.session.add(list_item_obj)
        product_obj = list_item_obj.product
        product_obj.in_stock_quantity = product_obj.in_stock_quantity - data['quantity']
        db.session.add(list_item_obj)
        db.session.commit()
        return list_item_obj


class PurchasedListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    purchased_by = fields.Nested(UserSchema, many=False, required=True)
    list = fields.Nested(ListSchema, many=False, required=True)
    list_item = fields.Nested(ListItemSchema, many=False, required=True)
    created_at = fields.DateTime(dump_only=True)

    @classmethod
    def create(cls, data, **kwargs):
        purchased_list_item_obj = PurchasedListItem(**data)
        db.session.add(purchased_list_item_obj)
        db.session.commit()
        return purchased_list_item_obj

