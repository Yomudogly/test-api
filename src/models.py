from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Sizes_shoes(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    brand_id = db.Column(db.Integer, nullable=True)
    sizes_types_id = db.Column(db.Unicode(10))
    cm = db.Column(db.Float(5,1))
    us = db.Column(db.Unicode(20))
    uk = db.Column(db.Unicode(20))
    europe = db.Column(db.Float(5,1))
    inch = db.Column(db.Float(5,1))
    woman = db.Column(db.Float(5,1), nullable=True)
    position = db.Column(db.Unicode(50), nullable=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.Unicode(100), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    
    product_details = db.relationship('Product_detail', backref='sizes_shoes', lazy=True)
    
    
    def __repr__(self):
        return (f'Size {self.cm}')
    
    def serialize(self):
        return {
            "id": self.id,
            "brandId": self.brand_id,
            "sizeTypeId": self.sizes_types_id,
            "cm": self.cm,
            "us": self.us,
            "uk": self.uk,
            "europe": self.europe,
            "inch": self.inch,
            "woman": self.woman,
            "position": self.position,
            "userId": self.user_id,
            "userName": self.user_name,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
        

class Product_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_id = db.Column(db.Integer)  #ForeignKey('product.id') !!!
    sizes_shoes_id = db.Column(db.Integer, ForeignKey('sizes_shoes.id'))
    sizes_shoes_val = db.Column(db.Float(18,1), nullable=True)
    lowest_ask = db.Column(db.Float(18,2), nullable=True)
    highest_offer = db.Column(db.Float(18,2), nullable=True)
    last_sale = db.Column(db.Float(18,2), nullable=True)
    last_sale_date = db.Column(db.DateTime, nullable=True)
    sales = db.Column(db.Integer, nullable=True, default=0)
    
    
    
    def __repr__(self):
        return (f'Product detail {self.slug}')
    
    def serialize(self):
        return {
            "id": self.id,
            "productId": self.product_id,
            "sizesShoesId": self.sizes_shoes_id,
            "sizesShoesVal": self.sizes_shoes_val,
            "lowestAsk": self.lowest_ask,
            "highestOffer": self.highest_offer,
            "lastSale": self.last_sale,
            "lastSaleDate": self.last_sale_date,
            "sales": self.sales
        }