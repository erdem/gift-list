from datetime import datetime

from app.database import db


class List(db.Model):
    # many-to-one User db model relation
    owner = db.relationship('User', back_populates="lists", uselist=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    list_items = db.relationship(
        'ListItem',
        back_populates='list',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    purchased_list_items = db.relationship(
        'PurchasedListItem',
        back_populates='list',
        lazy='dynamic',
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
    list = db.relationship('List', back_populates="list_items")
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    product = db.relationship('Product', back_populates="list_items", uselist=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    purchased_item = db.relationship(
        'PurchasedListItem',
        back_populates='list_item',
        cascade='all, delete-orphan',
        uselist=False
    )

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
    # one-to-one User db model relation
    purchased_by = db.relationship('User', back_populates="purchased_list_items")
    purchased_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # many-to-one List db model relation
    list = db.relationship('List', back_populates="purchased_list_items", uselist=False)
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'))

    # one-to-one ListItem model relation
    list_item = db.relationship('ListItem', back_populates="purchased_item")
    list_item_id = db.Column(db.Integer, db.ForeignKey('list_items.id'))

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
