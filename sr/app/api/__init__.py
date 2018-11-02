from flask import Blueprint, request, abort
import os
api = Blueprint('api', __name__)

@api.before_request
def before_request():
    api_key = os.environ.get('SR_API_KEY')
    req_api_key = request.headers.get('api_key')
    if  req_api_key is None or req_api_key is not api_key:
        abort(401)

#import dei file .py che contengono le view fun che ritornano le risorse indicate dal nome del file stesso
from . import users, stores, ecommerces, functions, prova
