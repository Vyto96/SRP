from flask import jsonify, redirect, request, url_for, json, make_response
from .. import db
from ..models import Store
from . import middle
import requests, os, base64
from urllib.parse import unquote, quote



@middle.route('/ebay/get_token')
def ebay_auth():
    url = os.environ.get('EBAY_RUNAME')
    return redirect(url)


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


@middle.route('/ebay/get_report')
def ebay_get_report():
    #HEADERS RICHIESTI A CHI USA L'API:
        #TOKEN DI AUTENTICAZIONE---> (validita' del token delegata ad'un altra API chiamata prima di questa)
    #PARAMS
    tk = request.headers.get('token')

    if tk:
        url_api = 'https://api.ebay.com/sell/analytics/v1/traffic_report'
        auth = 'Bearer ' + tk
        headers = { 'Authorization': auth }


        dim = 'DAY'
        mktp = 'EBAY_DE'
        start_date = '20181025'
        end_date = '20181022'

        params = {
            'dimension': dim, #DAY | #LISTING
            # 'sort': sort_field,
            'filter': {
                'marketplace_ids': '{'+ mktp +'}',
                'date_range': '[' + start_date + '..' + end_date + ']' #YYYYMMDD
            },
            'metric':[
                'TRANSACTION', # numero di transazioni completate
                'LISTING_VIEWS_TOTAL', # numero totale di annunci visualizzati
                'SALES_CONVERSION_RATE' # transazioni / visualizzazioni: ovvero quante delle effettive visualizzazioni diventano poi ordini
            ]

        }




        report = requests.get(url_api, headers=headers, params=params)

        return '<h1>report ricevuto:<br>{}</h1>'.format(report.text)

    return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url), 401


    # if token:
    #     return '<h1>TOKEN RICEVUTO</h1>'
    # return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url)
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
