from marshmallow import Schema, fields, post_load

from app.database import db
from app.products.models import Product


class ProductSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    brand = fields.String(required=True)
    price = fields.Decimal(required=True)
    in_stock_quantity = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)

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
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        self._instance = product
