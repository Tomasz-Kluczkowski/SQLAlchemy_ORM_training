from flask import Blueprint
from flask_restful import Api
from resources.hello import Hello
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Adds a new route
api.add_resource(Hello, '/hello')