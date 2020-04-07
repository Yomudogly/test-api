"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_restx import Api, Resource, abort
from flask_cors import CORS
from utils import APIException
from models import db, Sizes_shoes, Product_detail, Product, Brand, Model_cat
# import re
# from alembic import op
# from sqlalchemy import func


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='SnkrsDen API👟',
          version='v0.2',
          contact='SnkrsDen',
          contact_url='https://snkrsden.com',
          contact_email='info@snkrsden.com',
          description='''RESTFUL API
          
            📎 Comments and tips:
          
            ✓ For queries by multiple arguments you should pass them separated with + sign''',
          default='uncategorized',
          ordered=True)
app.register_blueprint(blueprint)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
# api.init_app(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


##### PAGINATION #####

def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj

#####################


pd = api.namespace('product-details', description='Operations related to product details table')
##### API PRODUCT DETAILS #######
@pd.route('')
class AllProductDetails(Resource):
    
    # GET ALL PRODUCT DETAILS
    @api.doc(responses={404: 'Product details not found', 200: 'Ok'})
    def get(self):
        products = Product_detail.query.all()
        products = list(map(lambda x: x.serialize(), products))
        
        return jsonify(get_paginated_list(products,
            '', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
        ))
        
#####  ID  ##### 
@pd.route('/<int:id>')
@api.doc(params={'id': 'id'})
# @api.tags(value={'name':'world'})
class ProductDetailsById(Resource):
    
    # PRODUCT DETAILS BY ID
    @api.doc(responses={404: 'Id not found', 200: 'Ok'})
    def get(self, id: int):
        
        products = Product_detail.query.get(id)
        if products:
            return jsonify(products.serialize())
        else: 
            abort (404, f'Product detail with id {id} does not exist')


#####  PRODUCT ID  #####
@pd.route('/product-id/<int:id>')
@api.doc(params={'id': 'integer'})
class ProductDetailsByProductId(Resource):
    
    # GET PRODUCT DETAILS BY PRODUCT ID
    @api.doc(responses={404: 'Product id not found', 200: 'Ok'})
    def get(self, id: int):
        products = Product_detail.query.filter_by(product_id=id).all()
        
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/product-id/{id}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            
#####  SIZES SHOES ID  #####
@pd.route('/sizes-id/<int:id>')
@api.doc(params={'id': 'integer'})
class ProductDetailsBySizesShoes(Resource):
    
    # GET PRODUCT DETAILS BY PRODUCT ID
    @api.doc(responses={404: 'Sizes shoes id not found', 200: 'Ok'})
    def get(self, id: int):
        products = Product_detail.query.filter_by(sizes_shoes_id=id).all()
        
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/sizes-id/{id}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            

##### SIZE #####
@pd.route('/size/<float:size>')
@api.doc(params={'size': 'float number in format x.x'})
class ProductDetailsBySize(Resource):
    
    # GET PRODUCT DETAILS BY SIZE
    @api.doc(responses={404: 'Size not found', 200: 'Ok'})
    def get(self, size: float):
        products = Product_detail.query.filter_by(sizes_shoes_val=size).all()
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/size/{size}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
             

#####  LOWEST ASK PRICE #####
@pd.route('/lowest-ask/<float:ask>')
@api.doc(params={'ask': 'float in format x.xx'})
class ProductDetailsByLowestAsk(Resource):
    
    # GET PRODUCT DETAILS BY LOWEST ASK PRICE
    @api.doc(responses={404: 'Lowest asking price not found', 200: 'Ok'})
    def get(self, ask: float):
        products = Product_detail.query.filter_by(lowest_ask=ask).all()
        # products = Product_detail.query.filter(Product_detail.lowest_ask<=ask) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/lowest-ask/{ask}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            
        
#####  HIGHEST OFFER  #####
@pd.route('/high-offer/<float:offer>')
@api.doc(params={'offer': 'float in format x.xx'})
class ProductDetailsByHighestOffer(Resource):
    
    # GET PRODUCT DETAILS BY HIGHEST OFFER
    @api.doc(responses={404: 'Highest offer not found', 200: 'Ok'})
    def get(self, offer: float):
        products = Product_detail.query.filter_by(highest_offer=offer).all()
        # products = Product_detail.query.filter(Product_detail.highest_offer<=offer) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/high-offer/{offer}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
 
                         
#####  LAST SALE PRICE #####
@pd.route('/last-sale/<float:last_sale>')
@api.doc(params={'last_sale': 'float in format x.xx'})
class ProductDetailsByLastSale(Resource):
    
    # GET PRODUCT DETAILS BY LAST SALE PRICE
    @api.doc(responses={404: 'Last sale price not found', 200: 'Ok'})
    def get(self, last_sale: float):
        products = Product_detail.query.filter_by(last_sale=last_sale).all()
        # products = Product_detail.query.filter(Product_detail.last_sale<=last_sale) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/last-sale/{last_sale}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            
#####  LAST SALE DATE #####
@pd.route('/last-sale-date/<string:date>')
@api.doc(params={'date': 'string in a format YYYY-MM-DD'})
class ProductDetailsByReleaseDate(Resource):
    # date should be a string in format "YYYY-MM-DD" to represent full date !!!
    # GET PRODUCT DETAILS BY RETAIL PRICE
    @api.doc(responses={404: 'Last sale date not found', 200: 'Ok'})
    def get(self, date: str):
        products = Product_detail.query.filter(Product_detail.last_sale_date.contains(date))
        # products = Product_detail.query.filter(Product_detail.last_sale_date<=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/last-sale-date/{date}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            
            
#####  SALES #####
@pd.route('/sales/<int:sales>')
@api.doc(params={'sales': 'integer'})
class ProductDetailsBySales(Resource):
    
    # GET PRODUCT DETAILS BY SALES
    @api.doc(responses={404: 'Sales not found', 200: 'Ok'})
    def get(self, sales: int):
        products = Product_detail.query.filter_by(sales=sales).all()
        # products = Product_detail.query.filter(Product_detail.sales<=sales) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                f'/sales/{sales}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)


#######################################################
#######################################################
########################################################


### API SIZES ###

sz = api.namespace('sizes', description='Operations related to sizes table')
@sz.route('')
class AllSizes(Resource):
    
    # GET ALL SIZES
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self):
        sizes = Sizes_shoes.query.all()
        sizes = list(map(lambda x: x.serialize(), sizes))
        
        return jsonify(get_paginated_list(sizes, '/sizes', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
    ))


@sz.route('/<int:id>')
@api.doc(params={'id': 'integer'})
class SizesById(Resource):
    
    # SIZES BY ID
    @api.doc(responses={404: 'Size not found', 200: 'Ok'})
    def get(self, id: int):
        size = Sizes_shoes.query.get(id)
        if size:
            return jsonify(size.serialize())
        else: 
            abort (404, f'Size with id {id} does not exist')
            

@sz.route('/brand-id/<int:brand_id>')
@api.doc(params={'brand_id': 'integer'})
class SizesByBrandId(Resource):
    
    # GET SIZES BY BRAND ID
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, brand_id: int):
        sizes = Sizes_shoes.query.filter_by(brand_id=brand_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/brand-id/{brand_id}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with brand id {brand_id} do not exist')
            

@sz.route('/type-id/<string:sizes_types_id>')
@api.doc(params={'sizes_types_id': 'string - m, w, td, gs, y or kids'})
class SizesByTypeId(Resource):
    
    # GET SIZES BY TYPE ID
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, sizes_types_id: str):
        sizes = Sizes_shoes.query.filter_by(sizes_types_id=sizes_types_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/type-id/{sizes_types_id}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with type id {sizes_types_id} do not exist')
  
 
@sz.route('/us/<string:us>')
@api.doc(params={'us': 'string in format number+letter or number+dot+number'})
class SizesByUS(Resource):
    
    # GET SIZES BY US
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, us: str):
        sizes = Sizes_shoes.query.filter_by(us=us).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/us/{us}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with us {us} do not exist')
        

@sz.route('/uk/<string:uk>')
@api.doc(params={'uk': 'string in format number+dot+number'})
class SizesByUK(Resource):
    
    # GET SIZES BY UK
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, uk: str):
        sizes = Sizes_shoes.query.filter_by(uk=uk).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/uk/{uk}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with uk {uk} do not exist')
    


@sz.route('/cm/<float:cm>')
@api.doc(params={'cm': 'float'})
class SizesByCM(Resource):
    
    # GET SIZES BY CM --  RQUIRES FLOAT NUMBER AS A PARAMETER
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, cm: float):
        sizes = Sizes_shoes.query.filter_by(cm=cm).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/cm/{cm}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with cm {cm} do not exist')
            
            
@sz.route('/europe/<float:europe>')
@api.doc(params={'europe': 'float'})
class SizesByEurope(Resource):
    
    # GET SIZES BY EUROPE --  RQUIRES FLOAT NUMBER AS A PARAMETER
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, europe: float):
        sizes = Sizes_shoes.query.filter_by(europe=europe).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/europe/{europe}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with europe size {europe} do not exist')
            
            
@sz.route('/inch/<float:inch>')
@api.doc(params={'inch': 'float'})
class SizesByInch(Resource):
    
    # GET SIZES BY INCH --  RQUIRES FLOAT NUMBER AS A PARAMETER
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, inch: float):
        sizes = Sizes_shoes.query.filter_by(inch=inch).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/inch/{inch}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with inch {inch} do not exist')
            
            
@sz.route('/woman/<float:woman>')
@api.doc(params={'woman': 'float'})
class SizesByWoman(Resource):
    
    # GET SIZES BY WOMAN --  RQUIRES FLOAT NUMBER AS A PARAMETER
    @api.doc(responses={404: 'Sizes not found', 200: 'Ok'})
    def get(self, woman: float):
        sizes = Sizes_shoes.query.filter_by(woman=woman).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(get_paginated_list(sizes, 
                f'/woman/{woman}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404, f'Sizes with woman size {woman} do not exist')



#######################################################
#######################################################
########################################################


### API PRODUCT ###

pr = api.namespace('products', description='Operations related to product table')
@pr.route('')
class AllProducts(Resource):
    
    # GET ALL PRODUCTS
    @api.doc(responses={404: 'Products not found', 200: 'Ok'})
    def get(self):
        products = Product.query.all()
        products = list(map(lambda x: x.serialize(), products))
        
        return jsonify(get_paginated_list(products, '/products', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
    ))
        
##### PRODUCTS BY BRAND SLUG AND MODEL SLUG #####
@pr.route('/<string:brand_slug>/<string:model_slug>', '/<string:brand_slug>')
@api.doc(params={'brand_slug': 'string'})
class ProductsByBrandAndModelSlug(Resource): 
    
    #### GET PRODUCT DETAILS BY SLUG ####
    @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
    def get(self, brand_slug: str, model_slug=None):
        
        brand = Brand.query.filter_by(slug=brand_slug).first() 
        model = Model_cat.query.filter_by(slug=model_slug).first()    
        if brand and not model:
            products = Product.query.filter_by(brand_id=brand.id).all()
            if products:
                products = list(map(lambda x: x.serialize(), products))
                        
                return jsonify(get_paginated_list(products,
                    f'/{brand_slug}', 
                    start=request.args.get('start', 1), 
                    limit=request.args.get('limit', 20)
                ))
            else:
                abort(404)  
        elif brand and model:
            products = Product.query.filter_by(brand_id=brand.id, model_cat_id=model.id).all()
            if products:
                products = list(map(lambda x: x.serialize(), products))
                        
                return jsonify(get_paginated_list(products,
                    f'/{brand_slug}/{model_slug}', 
                    start=request.args.get('start', 1), 
                    limit=request.args.get('limit', 20)
                ))
            else:
                abort(404)
        else: 
            abort(404)
            
            
##### PRODUCTS BY MODEL SLUG #####
@pr.route('/model/<string:model_slug>')
@api.doc(params={'model_slug': 'string'})
class ProductsByModelSlug(Resource): 
    
    #### GET PRODUCT DETAILS BY MODEL SLUG ####
    @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
    def get(self, model_slug: str):
        
        model = Model_cat.query.filter_by(slug=model_slug).first()    
        products = Product.query.filter_by(model_cat_id=model.id).all()
        if products:
            products = list(map(lambda x: x.serialize(), products))
                        
            return jsonify(get_paginated_list(products,
                f'/model/{model_slug}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else:
            abort(404)    
        
        
        
#######################################################
#######################################################
########################################################


### API BRAND ###

br = api.namespace('brands', description='Operations related to brand table')
@br.route('')
class AllBrands(Resource):
    
    # GET ALL BRANDS
    @api.doc(responses={404: 'Brands not found', 200: 'Ok'})
    def get(self):
        brands = Brand.query.all()
        brands = list(map(lambda x: x.serialize(), brands))
        
        return jsonify(get_paginated_list(brands, '/brands', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
    ))
        
        
        
#######################################################
#######################################################
########################################################


### API MODEL CATEGORY ###

mc = api.namespace('model-category', description='Operations related to model category table')
@mc.route('')
class AllModels(Resource):
    
    # GET ALL BRANDS
    @api.doc(responses={404: 'Models not found', 200: 'Ok'})
    def get(self):
        models = Model_cat.query.all()
        models = list(map(lambda x: x.serialize(), models))
        
        return jsonify(get_paginated_list(models, '/model-category', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
    ))
        



################ NEED TO CHECK ########################


# ##### SLUG #####
# @pd.route('/slug/<string:slug>')
# @api.doc(params={'slug': 'string in a format str+str1+str2'})
# class ProductDetailsBySlug(Resource): 
    
#     #### GET PRODUCT DETAILS BY SLUG ####
#     @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
#     def get(self, slug: str):
        
#         slug_ = list(slug.split("+"))
        
#         if len(slug_) is 1:
#             products = Product_detail.query.filter(Product_detail.slug.contains(slug_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.slug.contains(slug_[0]))
#             for i in range(1, len(slug_)):
#                 products = products.filter(Product_detail.slug.contains(slug_[i]))
            
#         if products:
#             products = list(map(lambda x: x.serialize(), products))
                    
#             return jsonify(get_paginated_list(products,
#                 f'/slug/{slug}', 
#                 start=request.args.get('start', 1), 
#                 limit=request.args.get('limit', 20)
#             ))
#         else: 
#             abort (404)
 

# ##### PRODUCT NAME #####
# @pd.route('/product-name/<string:name>')
# @api.doc(params={'name': 'string in a format str+str1+str2'})
# class ProductDetailsByProductName(Resource): 
    
#     #### GET PRODUCT DETAILS BY PRODUCT NAME ####
#     @api.doc(responses={404: 'Product name not found', 200: 'Ok'})
#     def get(self, name: str):
        
#         name_ = list(name.split("+"))
        
#         if len(name_) is 1:
#             products = Product_detail.query.filter(Product_detail.product_name.contains(name_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.product_name.contains(name_[0]))
#             for i in range(1, len(name_)):
#                 products = products.filter(Product_detail.product_name.contains(name_[i]))
            
#         if products:
#             products = list(map(lambda x: x.serialize(), products))
                    
#             return jsonify(get_paginated_list(products,
#                 f'/product-name/{name}', 
#                 start=request.args.get('start', 1), 
#                 limit=request.args.get('limit', 20)
#             ))
#         else: 
#             abort (404)                       
           

# ##### BRAND NAME #####
# @pd.route('/brand-name/<string:name>')
# @api.doc(params={'name': 'string in a format str+str1+str2'})
# class ProductDetailsByBrandName(Resource): 
    
#     #### GET PRODUCT DETAILS BY BRAND NAME ####
#     @api.doc(responses={404: 'Brand name not found', 200: 'Ok'})
#     def get(self, name: str):
        
#         name_ = list(name.split("+"))
        
#         if len(name_) is 1:
#             products = Product_detail.query.filter(Product_detail.brand_name.contains(name_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.brand_name.contains(name_[0]))
#             for i in range(1, len(name_)):
#                 products = products.filter(Product_detail.brand_name.contains(name_[i]))
            
#         if products:
#             products = list(map(lambda x: x.serialize(), products))
                    
#             return jsonify(get_paginated_list(products,
#                 f'/brand-name/{name}', 
#                 start=request.args.get('start', 1), 
#                 limit=request.args.get('limit', 20)
#             ))
#         else: 
#             abort (404) 
            
            
# ##### MODEL CATEGORY #####
# @pd.route('/category/<string:category>')
# @api.doc(params={'category': 'string in a format str+str1+str2'})
# class ProductDetailsByModelCategory(Resource): 
    
#     #### GET PRODUCT DETAILS BY MODEL CATEGORY ####
#     @api.doc(responses={404: 'Model category not found', 200: 'Ok'})
#     def get(self, category: str):
        
#         category_ = list(category.split("+"))
        
#         if len(category_) is 1:
#             products = Product_detail.query.filter(Product_detail.model_cat_name.contains(category_[0]))
#         else:
#             products = Product_detail.query.filter(Product_detail.model_cat_name.contains(category_[0]))
#             for i in range(1, len(category_)):
#                 products = products.filter(Product_detail.model_cat_name.contains(category_[i]))
            
#         if products:
#             products = list(map(lambda x: x.serialize(), products))
                    
#             return jsonify(get_paginated_list(products,
#                 f'/category/{category}', 
#                 start=request.args.get('start', 1), 
#                 limit=request.args.get('limit', 20)
#             ))
#         else: 
#             abort (404)




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
