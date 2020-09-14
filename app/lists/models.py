from datetime import datetime

from app.database import db


class List(db.Model):
    owner = db.relationship('users.User')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    items = db.relationship(
        'ListItem',
        back_populates='list',
        cascade='all, delete-orphan'
    )

    purchased_items = db.relationship(
        'PurchasedListItem',
        back_populates='list',
        cascade='all, delete-orphan'
    )

    __tablename__ = 'lists'

    def __str__(self):
        return (
            '<{class_name}('
            'owner_name={self.owner.name}, '
            'name="{self.name}")>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class ListItem(db.Model):
    list = db.relationship('lists.List')
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    product = db.relationship('Product')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __tablename__ = 'list_items'

    def __str__(self):
        return (
            '<{class_name}('
            'name={self.list.name})>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class PurchasedListItem(db.Model):
    purchased_by = db.relationship('users.User')
    purchased_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    list = db.relationship('List')
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    list_item = db.relationship('List')
    list_item_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __tablename__ = 'purchased_list_items'

    def __str__(self):
        return (
            '<{class_name}('
            'name={self.list.name})'
            'purchased_by={self.purchased_by.email}>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
