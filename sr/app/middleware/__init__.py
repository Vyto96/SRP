from flask import Blueprint

middle = Blueprint('middle', __name__)

from . import ebay #, altri ecommerce futuri...
