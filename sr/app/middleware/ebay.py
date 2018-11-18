from flask import jsonify, redirect, request, session
from . import middle
import requests, os
from urllib.parse import unquote, quote



@middle.route('/ebay/get_token', methods=['POST', 'GET'])
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

    r =requests.post(url, data=payload, headers=headers).json()
    return jsonify( r )



###################################################################################################################
# {
#   "access_token": "v^1.1#i^1#p^3#r^1...XzMjRV4xMjg0",
#   "expires_in": 7200,
#   "refresh_token": "v^1.1#i^1#p^3#r^1...zYjRV4xMjg0",
#   "refresh_token_expires_in": 47304000,
#   "token_type": "User Access Token"
# }
# {
#    "access_token": "v^1.1#i ... AjRV4yNjA=",
#    "expires_in": 7200,
#    "token_type":"User Access Token"
#  }

@middle.route('/ebay/refresh_token', methods=['POST'])
def ebay_refresh_token():
    refresh_token = request.form['refresh_token']

    url = 'https://api.ebay.com/identity/v1/oauth2/token'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': os.environ.get('EBAY_B64_CREDENTIAL')
    }

    #BODY
    payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'scope': os.environ.get('EBAY_SCOPE_LIST')
    }

    resp = requests.post(url, data=payload, headers=headers).json()

    return jsonify( access_token=resp['access_token'] )


@middle.route('/ebay/get_report')
def ebay_get_report():

    tk = request.headers.get('token')

    if tk:
        mktp = request.args['marketplace']
        start_date = request.args['start_date']
        end_date = request.args['end_date']

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

        if 'errors' in r.keys(): # error che indica l'aggiornamento del token
            return jsonify(error='ERRORE: ' + r.get('errors')[0]['message'] , error_code=401)

        start_report = r['startDate'][:10]
        end_report = r['endDate'][:10]
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

        return jsonify( start_report=start_report,
                        end_report=end_report,
                        report=report)
    else:
        return jsonify(error='token non ricevuto' , error_code=401)
