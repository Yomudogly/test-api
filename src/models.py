from flask_sqlalchemy import SQLAlchemy

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
    
    
    def __repr__(self):
        return (f'Size {self.cm}')
    
    def serialize(self):
        return {
            "Id": self.id,
            "BrandId": self.brand_id,
            "SizeTypeId": self.sizes_types_id,
            "CM": self.cm,
            "US": self.us,
            "UK": self.uk,
            "Europe": self.europe,
            "Inch": self.inch,
            "Woman": self.woman,
            "Position": self.position,
            "UserId": self.user_id,
            "UserName": self.user_name,
            "CreatedAt": self.created_at,
            "UpdatedAt": self.updated_at
        }
        

class Product_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    slug = db.Column(db.Unicode(200), nullable=True)
    colorway = db.Column(db.Unicode(100), nullable=True)
    style = db.Column(db.Unicode(100), nullable=True)
    retail_price = db.Column(db.Unicode(100), nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    model = db.Column(db.Unicode(200), nullable=True)
    size = db.Column(db.Float(11,1), nullable=True)
    last_sale = db.Column(db.Integer, nullable=True)
    last_sale_date = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return (f'Product detail {self.slug}')
    
    def serialize(self):
        return {
            "Id": self.id,
            "Slug": self.slug,
            "Colorway": self.colorway,
            "Style": self.style,
            "RetailPrice": self.retail_price,
            "ReleaseDate": self.release_date,
            "Model": self.model,
            "Size": self.size,
            "LastSale": self.last_sale,
            "LastSaleDate": self.last_sale_date
        }
    
# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<Person %r>' % self.username

#     def serialize(self):
#         return {
#             "username": self.username,
#             "email": self.email
#         }