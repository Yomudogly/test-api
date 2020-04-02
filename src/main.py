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
from models import db, Sizes_shoes, Product_detail
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
          tags=[{'name':'Product Details', 'description': 'all queries on product details'}],
          contact_email='info@snkrsden.com',
          description='''RESTFUL API
          
            📎 Comments and tips:
          
            ✓ For queries by multiple arguments you should pass them separated with + sign''',
          default='Available Endpoints',
          default_label=None,
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



##### API PRODUCT DETAILS #######
@api.route('/product-details')
class AllProductDetails(Resource):
    
    # GET ALL PRODUCT DETAILS
    @api.doc(responses={404: 'Id not found', 200: 'Ok'})
    def get(self):
        products = Product_detail.query.all()
        products = list(map(lambda x: x.serialize(), products))
        
        return jsonify(get_paginated_list(products,
            '/product-details', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
        ))
        
#####  ID  ##### 
@api.route('/product-details/<int:id>')
@api.doc(params={'id': 'An ID'})
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
 

##### SLUG #####
@api.route('/product-details/slug/<string:slug>')
@api.doc(params={'slug': 'string in a format str+str1+str2'})
class ProductDetailsBySlug(Resource): 
    
    #### GET PRODUCT DETAILS BY SLUG ####
    @api.doc(responses={404: 'Slug not found', 200: 'Ok'})
    def get(self, slug: str):
        
        slug_ = list(slug.split("+"))
        
        if len(slug_) is 1:
            products = Product_detail.query.filter(Product_detail.slug.contains(slug_[0]))
        else:
            products = Product_detail.query.filter(Product_detail.slug.contains(slug_[0]))
            for i in range(1, len(slug_)):
                products = products.filter(Product_detail.slug.contains(slug_[i]))
            
        if products:
            products = list(map(lambda x: x.serialize(), products))
                    
            return jsonify(get_paginated_list(products,
                f'/product-details/slug/{slug}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404)
 

##### COLORWAY #####
@api.route('/product-details/colorway/<string:colorway>')
class ProductDetailsByColorway(Resource): 
    
    #### GET PRODUCT DETAILS BY COLORWAY ####
    def get(self, colorway: str):
        
        colorway_ = list(colorway.split("+"))
        
        if len(colorway_) is 1:
            products = Product_detail.query.filter(Product_detail.colorway.contains(colorway_[0]))
        else:
            products = Product_detail.query.filter(Product_detail.colorway.contains(colorway_[0]))
            for i in range(1, len(colorway_)):
                products = products.filter(Product_detail.colorway.contains(colorway_[i]))
            
        if products:
            products = list(map(lambda x: x.serialize(), products))
                    
            return jsonify(get_paginated_list(products,
                f'/product-details/colorway/{colorway}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404)                       
           

##### STYLE #####
@api.route('/product-details/style/<string:style>')
class ProductDetailsByStlye(Resource): 
    
    #### GET PRODUCT DETAILS BY STYLE ####
    def get(self, style: str):
        
        style_ = list(style.split("+"))
        
        if len(style_) is 1:
            products = Product_detail.query.filter(Product_detail.style.contains(style_[0]))
        else:
            products = Product_detail.query.filter(Product_detail.style.contains(style_[0]))
            for i in range(1, len(style_)):
                products = products.filter(Product_detail.style.contains(style_[i]))
            
        if products:
            products = list(map(lambda x: x.serialize(), products))
                    
            return jsonify(get_paginated_list(products,
                f'/product-details/style/{style}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404) 
            
            
##### RETAIL PRICE #####
@api.route('/product-details/retail-price/<string:retail_price>')
class ProductDetailsByReatailPrice(Resource): 
    
    #### GET PRODUCT DETAILS BY RETAIL PRICE ####
    def get(self, retail_price: str):
        
        retail_price_ = list(retail_price.split("+"))
        
        if len(retail_price_) is 1:
            products = Product_detail.query.filter(Product_detail.retail_price.contains(retail_price_[0]))
        else:
            products = Product_detail.query.filter(Product_detail.retail_price.contains(retail_price_[0]))
            for i in range(1, len(retail_price_)):
                products = products.filter(Product_detail.retail_price.contains(retail_price_[i]))
            
        if products:
            products = list(map(lambda x: x.serialize(), products))
                    
            return jsonify(get_paginated_list(products,
                f'/product-details/retail-price/{retail_price}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404)
             

##### MODEL #####
@api.route('/product-details/model/<string:model>')
class ProductDetailsByModel(Resource): 
    
    ### GET PRODUCT DETAILS BY MODELS  ####
    def get(self, model: str):
        
        model_ = list(model.split("+"))
        
        if len(model_) is 1:
            products = Product_detail.query.filter(Product_detail.model.contains(model_[0]))
        else:
            products = Product_detail.query.filter(Product_detail.model.contains(model_[0]))
            for i in range(1, len(model_)):
                products = products.filter(Product_detail.model.contains(model_[i]))
            
        if products:
            products = list(map(lambda x: x.serialize(), products))
                    
            return jsonify(get_paginated_list(products,
                f'/product-details/model/{model}', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (404)
            
                
##### SIZE #####
@api.route('/product-details/size/<float:size>')
class ProductDetailsBySize(Resource):
    
    # GET PRODUCT DETAILS BY SIZE
    def get(self, size: float):
        products = Product_detail.query.filter_by(size=size).all()
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                '', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            
            
#####  LAST SALE PRICE #####
@api.route('/product-details/last-sale/<int:last_sale>')
class ProductDetailsByLastSale(Resource):
    
    # GET PRODUCT DETAILS BY LAST SALE PRICE
    def get(self, last_sale: int):
        products = Product_detail.query.filter_by(last_sale=last_sale).all()
        # products = Product_detail.query.filter(Product_detail.last_sale<=last_sale) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                '', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)

#####  RELEASE DATE #####
@api.route('/product-details/release-date/<string:release>')
class ProductDetailsByReleaseDate(Resource):
    # release should be a string in format "YYYY-MM-DD" to represent full date !!!
    # GET PRODUCT DETAILS BY RETAIL PRICE
    def get(self, release: str):
        products = Product_detail.query.filter(Product_detail.release_date.contains(release))
        # products = Product_detail.query.filter(Product_detail.release_date<=release) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                '', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)
            
#####  LAST SALE DATE #####
@api.route('/product-details/last-sale-date/<string:date>')
class ProductDetailsByReleaseDate(Resource):
    # date should be a string in format "YYYY-MM-DD" to represent full date !!!
    # GET PRODUCT DETAILS BY RETAIL PRICE
    def get(self, date: str):
        products = Product_detail.query.filter(Product_detail.last_sale_date.contains(date))
        # products = Product_detail.query.filter(Product_detail.last_sale_date<=date) -- for queries less then or more then !!!
        if products:
            products = list(map(lambda x: x.serialize(), products))
            
            return jsonify(get_paginated_list(products, 
                '', 
                start=request.args.get('start', 1), 
                limit=request.args.get('limit', 20)
            ))
        else: 
            abort (400)



### API SIZES ###

@api.route('/sizes')
class AllSizes(Resource):
    
    # GET ALL SIZES
    def get(self):
        sizes = Sizes_shoes.query.all()
        sizes = list(map(lambda x: x.serialize(), sizes))
        
        return jsonify(get_paginated_list(sizes, '/sizes', 
            start=request.args.get('start', 1), 
            limit=request.args.get('limit', 20)
    ))


@api.route('/sizes/<int:id>')
class SizesById(Resource):
    
    # SIZES BY ID
    def get(self, id: int):
        size = Sizes_shoes.query.get(id)
        if size:
            return jsonify(size.serialize())
        else: 
            abort (404, f'Size with id {id} does not exist')
            

@api.route('/sizes/brand-id/<int:brand_id>')
class SizesByBrandId(Resource):
    
    # GET SIZES BY BRAND ID
    def get(self, brand_id: int):
        sizes = Sizes_shoes.query.filter_by(brand_id=brand_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with brand id {brand_id} do not exist')
            

@api.route('/sizes/type-id/<string:sizes_types_id>')
class SizesByTypeId(Resource):
    
    # GET SIZES BY TYPE ID
    def get(self, sizes_types_id: str):
        sizes = Sizes_shoes.query.filter_by(sizes_types_id=sizes_types_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with type id {sizes_types_id} do not exist')
  
 
@api.route('/sizes/us/<string:us>')
class SizesByUS(Resource):
    
    # GET SIZES BY US
    def get(self, us: str):
        sizes = Sizes_shoes.query.filter_by(us=us).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with us {us} do not exist')
        

@api.route('/sizes/uk/<string:uk>')
class SizesByUK(Resource):
    
    # GET SIZES BY UK
    def get(self, uk: str):
        sizes = Sizes_shoes.query.filter_by(uk=uk).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with uk {uk} do not exist')
    


@api.route('/sizes/cm/<float:cm>')
class SizesByCM(Resource):
    
    # GET SIZES BY CM --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, cm: float):
        sizes = Sizes_shoes.query.filter_by(cm=cm).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with cm {cm} do not exist')
            
            
@api.route('/sizes/europe/<float:europe>')
class SizesByEurope(Resource):
    
    # GET SIZES BY EUROPE --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, europe: float):
        sizes = Sizes_shoes.query.filter_by(europe=europe).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with europe size {europe} do not exist')
            
            
@api.route('/sizes/inch/<float:inch>')
class SizesByInch(Resource):
    
    # GET SIZES BY INCH --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, inch: float):
        sizes = Sizes_shoes.query.filter_by(inch=inch).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with inch {inch} do not exist')
            
            
@api.route('/sizes/woman/<float:woman>')
class SizesByWoman(Resource):
    
    # GET SIZES BY WOMAN --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, woman: float):
        sizes = Sizes_shoes.query.filter_by(woman=woman).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with woman size {woman} do not exist')

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
