from app.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    price = db.Column(db.DECIMAL, nullable=False)
    in_stock_quantity = db.Column(db.Integer, index=True, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    __tablename__ = 'products'

    def __str__(self):
        return (
            '<{class_name}('
            'name={self.name})>'.format(
                class_name=self.__class__.__name__,
                self=self
            )
        )
