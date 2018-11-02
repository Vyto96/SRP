from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Store, User
from . import api
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
        return 'login successfull', 200
    else:
        return 'error: wrong password', 401


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

@api.route('/users/')
def get_users():
    users = User.query.all()
    if users:
        return jsonify( {'users': [u.to_json() for u in users] } )
    return '<h1>nessun utente nel db</h1>'

@api.route('/users/<username>/', methods=['GET', 'POST'])
def get_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET': # richiesta utente
        return jsonify( user.to_json() )
    else: # aggiungi utente
        return "<h1>aggiunta utente</h1>"

@api.route('/users/<id>/stores/')
def get_user_stores(id):
    stores = Store.query.filter_by(user_id=id).all()
    if stores:
        # return '<h1> user ha degli store configurati </h1><br>'
        return jsonify( {'user_stores': [s.to_json() for s in stores] } )
    else:
        return '<h1> user senza store configurati </h1><br>'
            # if user.stores:
    #     return '<h1> user esiste, tipo--></h1><br> ' +  str(type(str(user)))
    # else:
    #     return 'fuffa'
     # \
     #        + '<h1> tipo di user.stores </h1><br> ' + str(type(user.stores))
