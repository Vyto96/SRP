from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Store, User
from . import api
import requests, os
# from .decorators import permission_required
# from .errors import forbidden



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
    if  request.form.get('email') and \
        request.form.get('username') and \
        request.form.get('password'):
        user = User(email=request.form.get('email'),
                    username=request.form.get('username'),
                    password=request.form.get('password')
                         )
        db.session.add(user)
        db.session.commit()
        return 'Registration successful', 200
    return 'error', 401




@api.route('/user/<id_user>/ecommerce/<id_ecom>/add_stores', methods=['POST'])
def add_store(id_user, id_ecom):

    user = User.query.filter_by(id=id_user).first_or_404()
    ecommerce = Ecommerce.query.filter_by(id=id_ecom).first_or_404()
    store_name = request.form.get('store_name')

    if  store_name:
        url = os.environ.get('SR_HOME') + '/middle/ebay/get_token'
        payload = {
            "store_name": store_name,
            "id_user": id_user,
            "id_ecom": id_ecom
        }
        headers = {"return_url": "bla"}

        return requests.post(
            url = url,
            data = payload,
            headers = headers
            ).text

    return 'volevi', 404

    #
    #
    #
    #     user = User(email=request.form.get('email'),
    #                 username=request.form.get('username'),
    #                 password=request.form.get('password')
    #                      )
    #     db.session.add(user)
    #     db.session.commit()
    #     return 'Registration successful', 200
    # return 'error', 401









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


@api.route('/users/<id>/', methods=['GET', 'POST'])
def get_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET': # richiesta utente
        return jsonify( user.to_json() )
    else: # aggiungi utente
        return "<h1>aggiunta utente</h1>"



            # if user.stores:
    #     return '<h1> user esiste, tipo--></h1><br> ' +  str(type(str(user)))
    # else:
    #     return 'fuffa'
     # \
     #        + '<h1> tipo di user.stores </h1><br> ' + str(type(user.stores))
