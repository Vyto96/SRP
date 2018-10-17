from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Ecommerce, Store, Function
from . import api
# from .decorators import permission_required
# from .errors import forbidden


@api.route('/ecommerces/')
def get_ecommerces():
    
    return
