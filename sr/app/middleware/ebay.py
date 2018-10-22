from flask import jsonify, redirect, request, url_for, json
from .. import db
from ..models import Store
from . import middle
import requests, os, requests, base64

@middle.route('/ebay/get_token')
def ebay_auth():
    #url = request.form['access_url']
    url = os.environ.get('EBAY_RUNAME')
    # r = requests.get(url)
    return redirect(url)
    # return redirect(r.text)

@middle.route('/ebay/get_token/response/', methods=['GET', 'POST'])
def ebay_auth_code_response():
    # POST REQ per chiedere il token
    url = 'https://api.ebay.com/identity/v1/oauth2/token'
    #HEADER
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': os.environ.get('EBAY_B64_CREDENTIAL')
        }

    #BODY
    payload = {
                'grant_type': 'authorization_code',
                'code': request.args['code'],
                'redirect_uri': os.environ.get('EBAY_URI')
            }

    r = requests.post(url, data=payload, headers=headers)
    return r.json()
    # s = Store(store_name='Ebay', oauth_info=json.dumps( r.json() ))
    # db.session.add(s)
    # db.session.commit()

# devo fare load per far diventare json in dict e
#  poi dump per farla diventare stringa con eventuali valori NULL invece che none


@middle.route('/ebay/get_inventory')
def ebay_get_inventory():
    sr_home = os.environ.get('SR_HOME')
    token = requests.get(sr_home + '/ebay/get_token')
    if token:
        return '<h1>TOKEN RICEVUTO</h1>'
    return '<h1>TOKEN NON RICEVUTO</h1>'
