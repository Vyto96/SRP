from flask import jsonify, redirect, request, session
from . import middle
import requests, os
from urllib.parse import unquote, quote



@middle.route('/ebay/get_token', methods=['POST', 'GET'])
def ebay_auth():
    url = os.environ.get('EBAY_RUNAME')
    session['myadd'] = "fuffa"
    # session['return_url'] = request.form['return_url']
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
    r['myadd'] = session['myadd']

    return jsonify(r)



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




@middle.route('/ebay/prova')
def prova():

    UAtoken = {
        "access_token":"v^1.1#i^1#f^0#r^0#p^3#I^3#t^H4sIAAAAAAAAAOVYW2wUVRjutNuSgqVKiBfAuEzVIGR2z8zsbUZ245a2ttDL0l0aRBDOzJxpp52dWWbObLsQpZZAYipEkURCSC1BEonESAIaI1ESHySQSOKDxoSoIRK0gWJoFCMQndm2y7aGS1seNnFfduc///X7v//sOQN6y8qX7qzfeb2CmFU82At6iwmCngPKy0qXzS0pXlBaBPIUiMHep3tdfSW/LjdhUk3xrchM6ZqJ3D1JVTP5rDBMWobG69BUTF6DSWTyWOTj0aZGnvEAPmXoWBd1lXQ31IRJGiBZCAkikCCURQbYUm3cZ0IPk1JAZhDnC9LI+YFEe900LdSgmRhqOEwygA5RNKAYLkFzPMvxPuAJBZh1pLsNGaaia7aKB5CRbLp81tbIy/XuqULTRAa2nZCRhmhdvCXaUFPbnFjuzfMVGcMhjiG2zIlPK3QJudugaqG7hzGz2nzcEkVkmqQ3MhpholM+Op7MNNLPQs1JNMtwCAggyAowiB4IlHW6kYT47nk4EkWi5KwqjzSs4My9ELXREDqRiMeemm0XDTVu52u1BVVFVpARJmuroy+tide2ku54LGboaUVCUpZUPgb4AMcEGTKSzmCdC4xFGHUzhu+kECt0TVIctEx3s46rkZ0umgwKkweKrdSitRhRGTup5Okx9Dh4/tA6p5uj7bNwh+Y0FCVtBNzZx3tDP86F291/UGxgod8nAA76BU7y+cTQndjgzPpUGBFxmhKNxbxOLkiAGSoJjS6EUyoUESXa8FpJZCgSz/plhg3JiJICnEz5OFmmBL8UoGgZIYCQIIhc6H9BDIwNRbAwypFj8kK2ujDpgMkrUOax3oW0RCaFyMma2c1mjBE9ZpjswDjFe73d3d2ebtajG+1eBgDau7apMS52oCQkc7rKvZUpJcsN0d44bH0e2wmEyR6benZwrZ2MtNbWtdbG6zcmWlbVNo/TdkJmkcnSO1QaF/UUiumqImYKq0TWkGLQwJk4UlVbMKMiTafIwirPmXXHh2k7gSnF4zDOI+pJrw7t7coRbcxm7b4fJa9pg+QZHX7bu8dAUNI1NTMd4ynYKFraHiHdyEwnYM54CjZQFHVLw9MJN2Y6BQvZUmVFVZ1dYjoB88ynkqYG1QxWRDMXckbEj6ZSDcmkhaGgogapsCaABYw/96cw/fIKrKq0gm1SKzpln73TkIq11lCsM+sc6w8FmZCPggEpEAyI4owKb2pXCqxu2g8CHE2zgAOAmVFtNShdaE1lBRaEQFCiWIQ4yodEPwV9HEP5oV9GgBX8TMg/o5pXqIq9TxTeOaNeNzGSZlaafRIurKKcmRwfRzHgt8+L9mWX8klygBJ8Ik2xDH3f3ZwkiGPX0tzJ8j+3Ce/Ee3ykKPuh+4gToI84VkwQwAueoavA4rKSNa6ShxaYCkYe+xTqMZV2zb6eGsjThTIpqBjFZcTLiz4+sjHvzcHgBvB47t1BeQk9J+9FAlh0e6WUrnysgg7RgOFojuV8YB2our3qoh91zf/+6qmv/iw5VvFa28m/tm1t7NjCDp8DFTklgigtcvURRbt2f3Ag9Mq+TZ0bOg8NfQHIlWe3rY4M/36r/N3ZPQtXvnll9yOp7sUjI1XcocqBIXBtJDPv3PlPOw9bFVe2tH47nDaDpwe2X/ptQ1vlbP/Fxuv/vBGoOU1cnf/zH3vXvz2XuGR5yM+XnNiz/cXnH95f1xlM7Hjvo76TVU88uXnwuV9W9y06+oly63h1+tRTZP8Lu7c3ndWbnj187cIRInFw6HKE2gVvfbnsB544vKt/yaybZ965MbwgvoQ+ldg8Z8/5gyeW3xhBF183tokDsdk/9V/9en/TzX3HXw3s3TSw5puhrZfBhzvQZwsvrj3jcx2tk690vd+//4JUb61aG5i3/sDf3/1Y6Wp+Y/Nb1UOj7fsX2vcjldMRAAA=",
        "expires_in":7200,
        "refresh_token":"v^1.1#i^1#f^0#p^3#I^3#r^1#t^Ul4xMF82OkIwOUEzQjFDOTBEOUI5NUVDQzY1RThCREExQjE2Mjk1XzJfMSNFXjI2MA==",
        "refresh_token_expires_in":47304000,
        "token_type":"User Access Token"
    }

    tok = UAtoken['access_token']
    refresh_token = UAtoken['refresh_token']

    resp = requests.post(
                url="https://salesreporter.ddns.net/middle/ebay/refresh_token",
                data={'refresh_token': refresh_token}
                )

    ref_tok = resp.json()['access_token']

    url = 'https://salesreporter.ddns.net/middle/ebay/get_report'
    headers = {
        'token': tok
    }
    payload = {
        'marketplace':'EBAY_DE',
        'start_date':'20181020',
        'end_date':'20181029'
    }

    used_token = 'access_token'

    r = requests.get(url, headers=headers, params=payload)

    if 'error' in r.json().keys():
        #refresha token
        headers['token'] = ref_tok
        r = requests.get(url, headers=headers, params=payload)
        used_token = 'refresh_token'

    return jsonify( used_token=used_token, report=r.json() )

###################################################################################################################

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
