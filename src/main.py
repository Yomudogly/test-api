"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_restx import Api, Resource
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

# GET SIZES BY ID
@app.route('/sizes/<int:id>', methods=['GET'])
def get_sizes_by_id(id: int):
    sizes = Sizes_shoes.query.get(id)
    if sizes:
        return jsonify(sizes.serialize()), 200
    else: 
        return jsonify(message="Size with id " + str(id) + " do not exist"), 404
  
# GET SIZES BY US 
@app.route('/sizes-us/<string:us>', methods=['GET'])
def get_sizes_by_us(us: str):
    sizes = Sizes_shoes.query.filter_by(us=us).all()
    if sizes:
        sizes = list(map(lambda x: x.serialize(), sizes))
        return jsonify(sizes), 200
    else: 
        return jsonify(message="Size with us " + str(us) + " do not exist"), 404
    

# GET SIZES BY UK
@app.route('/sizes-uk/<string:uk>', methods=['GET'])
def get_sizes_by_uk(uk: str):
    sizes = Sizes_shoes.query.filter_by(uk=uk).all()
    if sizes:
        sizes = list(map(lambda x: x.serialize(), sizes))
        return jsonify(sizes), 200
    else: 
        return jsonify(message="Size with uk " + str(uk) + " do not exist"), 404
    

# GET SIZES BY CM --  RQUIRES FLOAT NUMBER AS A PARAMETER
@app.route('/sizes-cm/<float:cm>', methods=['GET'])
def get_sizes_by_cm(cm: float):
    sizes = Sizes_shoes.query.filter_by(cm=cm).all()
    if sizes:
        sizes = list(map(lambda x: x.serialize(), sizes))
        return jsonify(sizes), 200
    else: 
        return jsonify(message="Size with cm " + str(cm) + " do not exist"), 404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
