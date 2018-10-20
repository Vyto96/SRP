from flask import jsonify, redirect, request, url_for
from .. import db
from ..models import Store
from . import middle
import requests, os, requests, base64

@middle.route('/ebay/auth', methods=['GET', 'POST'])
def ebay_auth():
    #url = request.form['access_url']
    url = os.environ.get('EBAY_RUNAME')
    # r = requests.get(url)
    return redirect(url)
    # return redirect(r.text)




@middle.route('/ebay/auth_code/response/', methods=['GET', 'POST'])
def ebay_auth_code_response():
    # POST REQ per chiedere il token
    url = 'https://api.ebay.com/identity/v1/oauth2/token'

    #HEADER
    client_id = os.environ.get('EBAY_CLIENT_ID')
    client_secret = os.environ.get('EBAY_CLIENT_SECRET')
    s = 'Basic ' + client_id + ':' + client_secret
    s_b64 = base64.b64encode(s.encode('utf-8'))

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': s_b64,
        }

    #BODY
    g_type = 'authorization_code'
    auth_cod = request.args['code']
    ebay_uri = os.environ.get('EBAY_URI')
    payload = "grant_type=" + g_type + \
              "&code=" + auth_cod + \
              "&redirect_uri=" + ebay_uri

    response = requests.request("POST", url, data=payload, headers=headers)

    # s = Store(store_name='ebay.it', auth_code=cod)
    # db.session.add(s)
    # db.session.commit()
    response.
    return '<h1>json ricevuto == <br> {}</h1>'.format(response.headers)
