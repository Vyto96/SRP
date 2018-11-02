from flask import Blueprint, request, abort, url_for, redirec, session
import os
api = Blueprint('api', __name__)

@api.before_request
def before_request():
    api_key = os.environ.get('SR_API_KEY')
    req_api_key = request.headers.get('api_key')
    if  req_api_key is None or req_api_key != api_key:
        return 'api_key not valid', 401



# prova redirect
@api.route('/prova_redirect')
def prova_redirect():
    return 'se sei qui, sei stato redirectato e session = {}'.format(session['hello'])

# prova redirect
@api.route('/')
def index():
    session['hello'] = 'hello'
    return redirect(url_for('api.prova_redirect', _external=True))


#import dei file .py che contengono le view fun che ritornano le risorse indicate dal nome del file stesso
from . import users, stores, ecommerces, functions, prova
