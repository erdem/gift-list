from datetime import datetime

from app.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    brand = db.Column(db.String(32), nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    in_stock_quantity = db.Column(db.Integer, index=True, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    list_items = db.relationship(
        'ListItem',
        back_populates='product',
        cascade='all, delete-orphan'
    )

    __tablename__ = 'products'

    def __str__(self):
        return (
            '<{class_name}('
            'name={self.name})>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
