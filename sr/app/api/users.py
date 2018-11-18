from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Store, User
from . import api
import requests, os

@api.route('/login')
def try_login():
    logger = request.headers.get('logger')
    psw = request.headers.get('psw')

    if psw is None or logger is None:
        return 'data missed', 403

    user = User.query.filter_by(username=logger).first()
    if user is None:
        user = User.query.filter_by(email=logger).first()
        if user is None:
            return 'error: username or email not existing', 404

    if user.verify_password(psw):
        return jsonify( user.to_json() ), 200
    else:
        return jsonify( {} ), 401



@api.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    email_used = User.query.filter_by(email=email).first()
    if email_used:
        return 'error, email already used', 402

    username_used = User.query.filter_by(username=username).first()
    if username_used:
        return 'error, username already used', 403


    if  email and username and password:

        user = User(email=request.form.get('email'),
                    username=request.form.get('username'),
                    password=request.form.get('password')
                         )
        db.session.add(user)
        db.session.commit()
        return 'Registration successful', 200
    return 'error, data missed', 401


@api.route('/store_added_successfull')
def store_added():
    return '<h1>thanks to accept 3rd party condition!</h1> '

@api.route('/user/<id_user>/ecommerce/<id_ecom>/add_stores', methods=['POST'])
def add_store(id_user, id_ecom):

    store_name = request.form.get('store_name')
    if  store_name is None:
        abort(402)

    if session['new_store']['store_name'] == store_name and \
        session['new_store']['oauth_json']: # significa che add stores gia' e' stata chiamata
        #aggiungi store + token info
        s = Store(  store_name=store_name,
                    oauth_json=session['new_store']['oauth_json'],
                    user_id=session['new_store']['id_user'],
                    ecommerce_id=session['new_store']['id_ecom']
                     )
        db.session.add(s)
        db.session.commit()

        return url_for('api.store_added')

    else: #altrimenti pirma volta che vengo chiamato, necessito di token
        user = User.query.filter_by(id=id_user).first_or_404()
        ecommerce = Ecommerce.query.filter_by(id=id_ecom).first_or_404()

        session['new_store'] = {
            'store_name': store_name,
            "redirect_url": url_for('api.add_store', id_ecom, id_ecom, _external=True),
            "id_user": id_user,
            "id_ecom": id_ecom
        }

        redirect(url_for('middle.ebay_auth', _external=True) )








@api.route('/users/<id>/stores/')
def get_user_stores(id):
    stores = Store.query.filter_by(user_id=id).all()
    if stores:
        # return '<h1> user ha degli store configurati </h1><br>'
        return jsonify( {'user_stores': [s.to_json() for s in stores] } ), 200
    else:
        return jsonify({}), 404








@api.route('/users/')
def get_users():
    users = User.query.all()
    if users:
        return jsonify( {'users': [u.to_json() for u in users] } )
    return '<h1>nessun utente nel db</h1>'

# 
# @api.route('/users/<id>/', methods=['GET', 'POST'])
# def get_user(id):
#     user = User.query.get_or_404(id)
#     if request.method == 'GET': # richiesta utente
#         return jsonify( user.to_json() )
#     else: # aggiungi utente
#         return "<h1>aggiunta utente</h1>"
