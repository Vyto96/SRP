from flask import jsonify, request, url_for, current_app  #request, g,
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

#######da cancellare:
@api.route('/add_store',  methods=['POST'])
def add_store_simply():
    s = Store(
    store_name = request.form.get('store_name'),
    oauth_json = request.form.get('oauth_json'),
    user_id = 1,
    ecommerce_id = 1
    )
    db.session.add(s)
    db.session.commit()

    return jsonify(
        Store.query.filter_by(id=s.id).first().to_json()
    )
