from flask import jsonify, url_for, current_app  #request, g,
from .. import db
from ..models import Store, User, Ecommerce
from . import api



@api.route('/stores/')
def get_stores():
    stores = Store.query.all()
    if stores:
        return jsonify( {'stores': [s.to_json() for s in stores] } )
    return '<h1>nessuno store nel db</h1>'


@api.route('/stores/<id>')
def get_store(id):
    store = Store.query.get_or_404(id)
    return jsonify( store.to_json() )
