from marshmallow import Schema, fields

from app.database import db
from app.products.models import Product


class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    brand = fields.String(required=True)
    price = fields.String(required=True)
    in_stock_quantity = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)

    @classmethod
    def create(cls, data, **kwargs):
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return product
