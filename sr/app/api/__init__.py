from flask import Blueprint, request
import os
api = Blueprint('api', __name__)

@api.before_request
def before_request():
    api_key = os.environ.get('MY_API_KEY')
    if request.headers.get('api_key') is not api_key:
        return 'API key not valid', 401

#import dei file .py che contengono le view fun che ritornano le risorse indicate dal nome del file stesso
from . import users, stores, ecommerces, functions, prova
