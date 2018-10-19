from flask import jsonify, redirect, request, url_for
from .. import db
from . import middle
import requests

@middle.route('/ebay/auth_code/', methods=['GET', 'POST'])
def ebay_get_auth_code():
    #url = request.form['access_url']
    url = 'https://auth.ebay.com/oauth2/authorize?client_id=vittorio-prova-PRD-393587284-a6d676cc&response_type=code&redirect_uri=vittorio_Zavino-vittorio-prova--klgnkzvih&scope=https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.marketing.readonly https://api.ebay.com/oauth/api_scope/sell.marketing https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account.readonly https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly'
    # r = requests.get(url)
    return redirect(url)
    # return redirect(r.text)



@middle.route('/ebay/auth_code/response/', methods=['GET', 'POST'])
def ebay_auth_code_response():
    cod = request.args['prova']
    return '<h1>codice ricevuto == {}</h1>'.format(cod)
