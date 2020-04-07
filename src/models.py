from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT, TINYINT

db = SQLAlchemy()


class Sizes_shoes(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    brand_id = db.Column(db.Integer, ForeignKey('brand.id'))
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
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
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
        
        
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Unicode(100))
    brand_id = db.Column(db.Integer, ForeignKey('brand.id'))
    brand_name = db.Column(db.Unicode(50), nullable=True) # DUPLICAT of Brand row
    model_cat_id = db.Column(db.Integer, ForeignKey('model_cat.id'))
    model_cat_name = db.Column(db.Unicode(200), nullable=True) # DUPLICAT of Model_cat row
    brief_description = db.Column(LONGTEXT, nullable=True)
    description = db.Column(LONGTEXT, nullable=True)
    retail_price = db.Column(db.Float(18,2), nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    colorway = db.Column(db.Unicode(100), nullable=True)
    style = db.Column(db.Unicode(100), nullable=True)
    weight = db.Column(db.Float(18,2), nullable=True)
    length = db.Column(db.Float(18,2), nullable=True)
    width = db.Column(db.Float(18,2), nullable=True)
    height = db.Column(db.Float(18,2), nullable=True)
    visit = db.Column(db.Integer, default=1)
    recent_view = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(TINYINT(1), default=1, nullable=True)
    seo_title = db.Column(db.Unicode(60), nullable=True)
    seo_description = db.Column(db.Unicode(160), nullable=True)
    seo_keywords = db.Column(LONGTEXT, nullable=True)
    lowest_ask = db.Column(db.Float(18,2), nullable=True) 
    highest_offer = db.Column(db.Float(18,2), nullable=True)
    most_recent = db.Column(db.Float(18,2), nullable=True) 
    image = db.Column(db.Unicode(100), nullable=True)
    recently_viewed = db.Column(db.DateTime, nullable=True)  # WILL KEEP INSTEAD OF recent_view
    user_id = db.Column(db.Integer, nullable=True)   # ForeignKey('sf_guard_user.id')
    user_name = db.Column(db.Unicode(100), nullable=True) # DUPLICAT of sf_guard_user row ???
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    slug = db.Column(db.Unicode(255), nullable=True)
    
    product_details = db.relationship('Product_detail', backref='product', lazy=True)
    
    
    def __repr__(self):
        return (f'Product {self.name}')
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "brandId": self.brand_id,
            "brandName": self.brand_name,
            "modelCatId": self.model_cat_id,
            "modelCatName": self.model_cat_name,
            "briefDesc": self.brief_description,
            "description": self.description,
            "retailPrice": self.retail_price,
            "releaseDate": self.release_date,
            "colorway": self.colorway,
            "style": self.style,
            "weight": self.weight,
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "visit": self.visit,
            "recentView": self.recent_view,
            "isActive": self.is_active,
            "seoTitle": self.seo_title,
            "seoDesc": self.seo_description,
            "seoKeywords": self.seo_keywords,
            "lowestAsk": self.lowest_ask,
            "highestOffer": self.highest_offer,
            "mostRecent": self.most_recent,
            "image": self.image,
            "recentlyViewed": self.recently_viewed,
            "userId": self.user_id,
            "userName": self.user_name,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "slug": self.slug 
        }
        
        
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    brand_id =  db.Column(db.Integer, default=0, nullable=True)  # WHY ???
    name = db.Column(db.Unicode(100))
    description = db.Column(LONGTEXT, nullable=True)  #  ??? OR DUPLICAT OF PRODUCT ROW  
    seo_title = db.Column(db.Unicode(60), nullable=True)   # DUPLICAT OF PRODUCT ROW
    seo_description = db.Column(db.Unicode(160), nullable=True)  # DUPLICAT OF PRODUCT ROW
    seo_keywords = db.Column(LONGTEXT, nullable=True)  # DUPLICAT OF PRODUCT ROW
    shortcut =  db.Column(db.Unicode(200), nullable=True)
    image = db.Column(db.Unicode(100), nullable=True)
    favicon = db.Column(db.Unicode(100), nullable=True)
    user_id = db.Column(db.Integer)      # ForeignKey('sf_guard_user.id')
    status = db.Column(db.Integer, default=0, nullable=True)
    rep_popular_brand = db.Column(db.Integer, default=0, nullable=True)
    posicion_order = db.Column(db.Integer, default=0, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    slug = db.Column(db.Unicode(255), nullable=True)
    
    product = db.relationship('Product', backref='brand', lazy=True)
    sizes_shoes = db.relationship('Sizes_shoes', backref='brand', lazy=True)
    model_cat = db.relationship('Model_cat', backref='brand', lazy=True)
    
    def __repr__(self):
        return (f'Brand {self.name}')
    
    def serialize(self):
        return {
            "id": self.id,
            "brandId": self.brand_id,
            "name": self.name,
            "description": self.description,
            "seoTitle": self.seo_title,
            "seoDesc": self.seo_description,
            "seoKeywords": self.seo_keywords,
            "shortcut": self.shortcut,
            "image": self.image,
            "favicon": self.favicon,
            "userId": self.user_id,
            "status": self.status,
            "repPopularBrand": self.rep_popular_brand,
            "positionOrder": self.posicion_order,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "slug": self.slug 
        }
        
        
class Model_cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    brand_id = db.Column(db.Integer, ForeignKey('brand.id'))
    model_cat_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.Unicode(100))
    slug_full = db.Column(db.Unicode(250), nullable=True)
    description = db.Column(LONGTEXT, nullable=True)
    seo_title = db.Column(db.Unicode(60), nullable=True)
    seo_description = db.Column(db.Unicode(160), nullable=True)
    seo_keywords = db.Column(LONGTEXT, nullable=True)
    shortcut = db.Column(db.Unicode(200), nullable=True)
    image = db.Column(db.Unicode(100), nullable=True)
    favicon = db.Column(db.Unicode(100), nullable=True)
    user_id = db.Column(db.Integer)      # ForeignKey('sf_guard_user.id')
    status = db.Column(db.Integer, default=0, nullable=True)
    rep_popular_brand = db.Column(db.Integer, default=0, nullable=True)
    posicion_order = db.Column(db.Integer, default=0, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    slug = db.Column(db.Unicode(255), nullable=True)
    
    product = db.relationship('Product', backref='model_cat', lazy=True)
    
    def __repr__(self):
        return (f'Model category {self.name}')
    
    def serialize(self):
        return {
            "id": self.id,
            "brandId": self.brand_id,
            "modelCatId": self.model_cat_id,
            "name": self.name,
            "slugFull": self.slug_full,
            "description": self.description,
            "seoTitle": self.seo_title,
            "seoDesc": self.seo_description,
            "seoKeywords": self.seo_keywords,
            "shortcut": self.shortcut,
            "image": self.image,
            "favicon": self.favicon,
            "userId": self.user_id,
            "status": self.status,
            "repPopularBrand": self.rep_popular_brand,
            "positionOrder": self.posicion_order,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "slug": self.slug
        }