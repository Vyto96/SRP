from flask import Blueprint

api = Blueprint('api', __name__)

#import dei file .py che contengono le view fun che ritornano le risorse indicate dal nome del file stesso
from . import users, stores, ecommerces, functions, prova
