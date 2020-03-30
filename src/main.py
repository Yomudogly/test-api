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
from models import db, Sizes_shoes


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='SnkrsDen API',
          version='v0.1',
          description='RESTful API',
          default='Available Methods/Endpoints',
          default_label=None)
app.register_blueprint(blueprint)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
# api.init_app(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code




### API SIZES ###

@api.route('/sizes')
class AllSizes(Resource):
    
    # GET ALL SIZES
    def get(self):
        sizes = Sizes_shoes.query.all()
        sizes = list(map(lambda x: x.serialize(), sizes))

        return jsonify(sizes)


@api.route('/sizes/<int:id>')
class SizesById(Resource):
    
    # SIZES BY ID
    def get(self, id: int):
        size = Sizes_shoes.query.get(id)
        if size:
            return jsonify(size.serialize())
        else: 
            abort (404, f'Size with id {id} does not exist')
            

@api.route('/sizes-brand-id/<int:brand_id>')
class SizesByBrandId(Resource):
    
    # GET SIZES BY BRAND ID
    def get(self, brand_id: int):
        sizes = Sizes_shoes.query.filter_by(brand_id=brand_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with brand id {brand_id} do not exist')
            

@api.route('/sizes-type-id/<string:sizes_types_id>')
class SizesByTypeId(Resource):
    
    # GET SIZES BY TYPE ID
    def get(self, sizes_types_id: str):
        sizes = Sizes_shoes.query.filter_by(sizes_types_id=sizes_types_id).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with type id {sizes_types_id} do not exist')
  
 
@api.route('/sizes-us/<string:us>')
class SizesByUS(Resource):
    
    # GET SIZES BY US
    def get(self, us: str):
        sizes = Sizes_shoes.query.filter_by(us=us).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with us {us} do not exist')
        

@api.route('/sizes-uk/<string:uk>')
class SizesByUK(Resource):
    
    # GET SIZES BY UK
    def get(self, uk: str):
        sizes = Sizes_shoes.query.filter_by(uk=uk).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with uk {uk} do not exist')
    


@api.route('/sizes-cm/<float:cm>')
class SizesByCM(Resource):
    
    # GET SIZES BY CM --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, cm: float):
        sizes = Sizes_shoes.query.filter_by(cm=cm).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with cm {cm} do not exist')
            
            
@api.route('/sizes-europe/<float:europe>')
class SizesByEurope(Resource):
    
    # GET SIZES BY EUROPE --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, europe: float):
        sizes = Sizes_shoes.query.filter_by(europe=europe).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with europe size {europe} do not exist')
            
            
@api.route('/sizes-inch/<float:inch>')
class SizesByInch(Resource):
    
    # GET SIZES BY INCH --  RQUIRES FLOAT NUMBER AS A PARAMETER
    def get(self, inch: float):
        sizes = Sizes_shoes.query.filter_by(inch=inch).all()
        if sizes:
            sizes = list(map(lambda x: x.serialize(), sizes))
            return jsonify(sizes)
        else: 
            abort (404, f'Sizes with inch {inch} do not exist')
            
            
@api.route('/sizes-woman/<float:woman>')
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
