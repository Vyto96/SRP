from flask import jsonify, redirect, request, url_for,
from .. import db
from ..models import Store
from . import middle
import requests, os, requests, base64

@middle.route('/ebay/auth', methods=['GET', 'POST'])
def ebay_auth():
    #url = request.form['access_url']
    url = os.environ.get('EBAY_URI')
    # r = requests.get(url)
    return redirect(url)
    # return redirect(r.text)




@middle.route('/ebay/auth_code/response/', methods=['GET', 'POST'])
def ebay_auth_code_response():
    cod = request.args['code']

    url = 'https://api.ebay.com/identity/v1/oauth2/token'
     
    s_b = s.encode('utf-8')
    s_b64 = base64.b64encode(s_b)

    r = requests.post(url=)

    # s = Store(store_name='ebay.it', auth_code=cod)
    db.session.add(s)
    db.session.commit()
    return '<h1>codice ricevuto == {}</h1>'.format(cod)
