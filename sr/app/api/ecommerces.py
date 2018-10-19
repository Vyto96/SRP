from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Ecommerce, Store, Function
from . import api
# from .decorators import permission_required
# from .errors import forbidden


@api.route('/ecommerces/')
def get_ecommerces():
    ecoms = Ecommerce.query.all()
    if ecoms:
        return jsonify( {'ecommerces': [e.to_json() for e in ecoms] } )
    return '<h1>nessuno ecommerce nel db</h1>'
