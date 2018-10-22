from flask import jsonify, redirect, request, url_for, json, make_response
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

    return requests.post(url, data=payload, headers=headers).text
    # s = Store(store_name='Ebay', oauth_info=json.dumps( r.json() ))
    # db.session.add(s)
    # db.session.commit()

# devo fare load per far diventare json in dict e
#  poi dump per farla diventare stringa con eventuali valori NULL invece che none

  #
  # {
  #   "access_token": "v^1.1#i^1#p^3#r^1...XzMjRV4xMjg0",
  #   "expires_in": 7200,
  #   "refresh_token": "v^1.1#i^1#p^3#r^1...zYjRV4xMjg0",
  #   "refresh_token_expires_in": 47304000,
  #   "token_type": "User Access Token"
  # }

@middle.route('/ebay/get_inventory')
def ebay_get_inventory():
    url = os.environ.get('SR_HOME')  + '/middle/ebay/get_token'
    token = requests.get(url)

    url_api = ' https://api.ebay.com/sell/inventory/v1/inventory_item'
    auth = 'Bearer ' + str(token['access_token'])
    headers = {
            'Authorization': auth
    }
    payload = {
            'offset': 0,
            'limit': 2
    }

    inventory = requests.get(url, headers=headers, params=payload)

    return '<h1>primi due oggetti dell inventario:<br>{}</h1>'.format(inventory.text)

    # if token:
    #     return '<h1>TOKEN RICEVUTO</h1>'
    # return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url)
