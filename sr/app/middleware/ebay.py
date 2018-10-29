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

    resp = json.loads( requests.post(url, data=payload, headers=headers).text )

    return jsonify( access_token=resp['access_token'] )




@middle.route('/ebay/prova')
def hello():
    tok = "v^1.1#i^1#f^0#r^0#p^3#I^3#t^H4sIAAAAAAAAAOVYbWgTZxxv0pdRtAqjvuDciKeiqJc8d5e75G4mLPYFozWNTRWt2Prc3XPNzctduHvSGueg1qHgQMYodludKw7GlH2YY+6lOrcxZVMYFebGQJjuy9YPw0nBORm43aVtmtZNbeuHwPIl3PP8336//+//8NyBrorKVQfXH7xT5XrC3d8FutwuFzULVFaUr55T6l5UXgIKDFz9Xcu6yrpLh9ZaMKWlhSZkpQ3dQp49KU23hNxiiMiYumBAS7UEHaaQJWBJSEQ2NQi0Fwhp08CGZGiEJ1obIvwyI/NQCUiijBSa5uxVfSxmsxEieJYPSGyAlVhO4hSFtvctK4OiuoWhjkMEDaggSQGS5pspXgBAYIDXHwy0EJ6tyLRUQ7dNvIAI58oVcr5mQa0PLhVaFjKxHYQIRyP1icZItLYu1rzWVxArPMpDAkOcsSY+1Rgy8myFWgY9OI2VsxYSGUlClkX4wiMZJgYVImPFTKP8HNUixwBG4UWGBbwSAI+FyXrDTEH84DKcFVUmlZypgHSs4uzDCLXJEJ9HEh59itkhorUe529zBmqqoiIzRNSti2zfkqhrIjyJeNw0OlQZyQ5Qyk+zAS5AUTwRTmbTyHRSU+xompFYoxxPylNj6LLqMGZ5YgZeh2xHNJGZoMAWMGMbNeqNZkTBTj0FdjSVZ9Df4nR0pIUZnNSdpqKUTYMn9/hw/sf0MK6Ax6UICvIyS7H+AMsgGIDBf5OEM+tTlUXY6UwkHvc5tSARZskUNHcjnNaghEjJpjeTQqYqCwyr0ExQQaTM8Qrp5xWFFFmZIykFIYCQKEp88P+jDoxNVcxglFfI5I0cxBDhMCqoUBGwsRvpzTYGYrJl7tQZlcUeK0QkMU4LPl9nZ6e3k/EaZruPBoDybdvUkJCSKAWJvK36cGNSzQlEQraXpQrYLiBE7LH1ZyfX24lwU119U11ifVtz48a62Jh2J1QWnrz6H0gTkpFGcUNTpWxxQWRMOQ5NnE0gTbMXZgTSckAWBTxn1vMQnRiWHQSmVa+jOK9kpHwGtM8sZ6ktV7XnUYx8lk2Sd+QEsCN7TQRlQ9ey03Gego+qd9gjZJjZ6STMO0/BB0qSkdHxdNKNuk7BQ8loiqppzikxnYQF7lMpU4daFquSlU85I+FH0uloKpXBUNRQVC6KCRgfcECzPDdjeEWGqkPFtqhVg0ybzqwbHZCMN9WSDM+wwQAd9JOQk7kAJ0kzAr6pXS0y3BRL2Q3lGC4IQHBG2GpRR7E1lREZEAQBmWQQ4kk/klgS+nmaZCGrIMCILB1kZ4S5RlPtc6L47hnrDQsjeWbQ7OtwcYFy5nFsHCWOte+LCEmkX1Y4UvRLFMnQ1CN3c2yhjLn/ZnnfK4Vv4gt9uCT3o7pdZ0C367Tb5QI+sJxaCpZUlG4pK529yFIx8tq3UK+ltuv2e6qJvLtRNg1V013h2rH4/ZNtBZ8Q+neChfmPCJWl1KyCLwpg8fhOOTV3QRUVpADNUzwADGgBS8d3y6j5ZdWHxRVe8+t43FjTvFP+40Li2u0DraAqb+RylZeUdbtK2u4ec717+6509tu9r+jVV78Y9pPe/nM9x15eOXfw7i/PLG+sbj1wvGHHhuyaEy9+TtbdUJPnrsTe3PUNsfbHYZVl5x3a/97Cs6tulvbu3PfavL/euNmrvXAYn1rtvnRkV2tPbZgcLOn7+NpXAwv+3FCe0j+40Hqru3rJjeShq0d7T3uOvPRW36+xt+fQ1rpzlRd3rYjGKLUmLPrn/zbI9PDhE3Nl7vt9P9w5GbuXeHb/xeSpvuFXk0/t7y/77KfNX157Z6CZOXrgev31j3o+EfXjpz/98HJ0qD/rH3r9zDZt7wngG/juUuP5wYbL7nj7YMutjeefvLfS/TtJ/z37yvZTVfHh554eWvbzQO9I+/4BCSXWqdwRAAA="

    refresh_token = "v^1.1#i^1#I^3#p^3#r^1#f^0#t^Ul4xMF82OjkwRkNDNzY5NzUzODg2QjgzODVGQTdFMzI4MTg5NzIwXzJfMSNFXjI2MA=="

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
        mktp = request.args['marketplace'] #request.headers.get
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

        if 'errors' in r.keys():
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
