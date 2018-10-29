from flask import jsonify, redirect, request, json
from .. import db
from ..models import Store
from . import middle
import requests, os
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


# @middle.route('/ebay/verify_token', methods=['POST'])
# def ebay_verify_token():






###################################################################################################################à


@middle.route('/ebay/get_report')
def ebay_get_report():
    #HEADERS RICHIESTI A CHI USA L'API:
    # TODO:     #TOKEN DI AUTENTICAZIONE---> (validita' del token delegata ad'un altra API chiamata prima di questa)
    #PARAMS
    UAtoken = json.loads( request.headers.get('UAtoken') )

    if not UAtoken:
        return jsonify(error='User Access token non ricevuto', error_code=401)

    tk = UAtoken['access_token']

  # {
  #   "access_token": "v^1.1#i^1#p^3#r^1...XzMjRV4xMjg0",
  #   "expires_in": 7200,
  #   "refresh_token": "v^1.1#i^1#p^3#r^1...zYjRV4xMjg0",
  #   "refresh_token_expires_in": 47304000,
  #   "token_type": "User Access Token"
  # }

    mktp = request.headers.get('marketplace') #request.headers.get
    start_date = request.headers.get('start_date')
    end_date = request.headers.get('end_date')


    url_api = 'https://api.ebay.com/sell/analytics/v1/traffic_report'
    auth = 'Bearer ' + tk
    headers = { 'Authorization': auth }
    dim = 'DAY'

    params = {
        "filter": 'marketplace_ids:{' + mktp + '},date_range:[' + start_date + '..' + end_date +']',
        "dimension": dim,
        "metric": "LISTING_VIEWS_TOTAL,TRANSACTION,SALES_CONVERSION_RATE"
    }

    response = requests.get(url_api, headers=headers, params=params)

    r = response.json()

    if 'errors' in r.keys():
        return jsonify(error=r.get('errors')[0]['message'] , error_code=401)

    report = []
    for i in r['records']:
        date = i['dimensionValues'][0]['value']
        date = date[:4] + '/' + date[4:6] + '/' + date[6:8]
        tot_views = i['metricValues'][0]['value']
        transactions = i['metricValues'][1]['value']
        scr = i['metricValues'][2]['value'] #SALES_CONVERSION_RATE

        report.append({ 'date': date,
                        'tot_views': tot_views,
                        'transactions': transactions,
                        'scr': scr
                        })

    return jsonify(report=report, 200)







    # s = Store(store_name='Ebay', oauth_info=json.dumps( r.json() ))
    # db.session.add(s)
    # db.session.commit()

# devo fare load per far diventare json in dict e
#  poi dump per farla diventare stringa con eventuali valori NULL invece che none


  # {
  #   "access_token": "v^1.1#i^1#p^3#r^1...XzMjRV4xMjg0",
  #   "expires_in": 7200,
  #   "refresh_token": "v^1.1#i^1#p^3#r^1...zYjRV4xMjg0",
  #   "refresh_token_expires_in": 47304000,
  #   "token_type": "User Access Token"
  # }
