from flask import Blueprint

middle = Blueprint('middle', __name__)

#import dei file .py che contengono le view fun che ritornano le risorse indicate dal nome del file stesso
from . import ebay #, altri ecommerce futuri...
