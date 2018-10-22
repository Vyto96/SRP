from flask import jsonify, redirect, request, url_for, json, make_response
from .. import db
from ..models import Store
from . import middle
import requests, os, base64

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

    token =  {"access_token":"v^1.1#i^1#I^3#f^0#p^3#r^0#t^H4sIAAAAAAAAAOVYW2wUVRju9qYEqxgrEKjJOhRQZHbPXHd30l3dtltboe2yW5Cr9czMmXZgdmaZOdt2iWJZCcEL0YBoiCRUJEZADT70RRN9AGPA8OIl8QXFBLThovFFwJjgmW27bGu4tOWhifOymf/8t+/7///sOQP6K2cs2dG840qV557SgX7QX+rxMDPBjMqKJ+4vK51XUQKKFDwD/bX95bmyoToHpoy0lEBO2jId5O1LGaYj5YVhKmObkgUd3ZFMmEKOhBUpGW1dLrE+IKVtC1uKZVDelsYwxUOVgzxSGE0MCDIXIFJz1GeHFaZUBDWGRSrLhpDMhCBZd5wMajEdDE0cpljABGkG0CzbwfASF5R4zsewwlrKuwrZjm6ZRMUHqEg+XSlvaxfleutUoeMgGxMnVKQl2pRsj7Y0xto66vxFviIjPCQxxBln7FuDpSLvKmhk0K3DOHltKZlRFOQ4lD8yHGGsUyk6mswk0s9TLXOI01CIF0RWFslzV6hssuwUxLfOw5XoKq3lVSVkYh1nb8coYUPeiBQ88tZGXLQ0et2fFRlo6JqO7DAVq4+uWZmMJShvMh63rR5dRaqLlOFZwIMQG2CpSE8WWyFxJMKwmxF+x4VosExVd9lyvG0WrkckXTSeFLaIFKLUbrbbUQ27qRTriQXymLVuNYfLl8HdpltQlCIMePOvt6d+tBduVP9udYPCiJys8AIfRLwmo5sOljvrE+mIiFuUaDzud3NBMszSKWhvQjhtQAXRCqE3k0K2rkqcoLFcUEO0KoY0mg9pGi0LqkgzGkIAIVlWQsH/RWNgbOtyBqNCc4xfyKMLUy6Zkg41CVubkNmRTSNqvGZ+sxnpiD4nTHVjnJb8/t7eXl8v57PsLj8LAONf3bo8qXSjFCn6qK5+e2Vaz/eGgoiVo0uYJBCm+kjrkeBmFxVJxJoSsWRzZ0f7sljbaNuOySwyXnoTpEnFSqO4ZehKdnpB5Gw1Dm2cTSLDIIIpgXRckNMLnjvrrg+HOIFp3ed2nE+xUn4Lku3KFXXms/beiZLfIST5hoefePfZCKqWaWQnYzwBG93sISNk2dnJBCwYT8AGKoqVMfFkwo2YTsBCyxiabhjuLjGZgEXmE0nThEYW64pTCDmlxo+m0y2pVAZD2UAt6vSaAA6wQuFPYfLwphmqHh2TptYtmpy9eyAdTzTSnDvrIU4IBtggT0NRFQOiokwJeGuXPs1wMwIQQwzDgRAA7JSwNaKe6VZUTuZAEARUmkMoRJMrlEBDPsTSAhQ0BDhZYIPClDA3GDrZJ6bfOaPZcjBSpwaNnISnFyh3JkfHUREFcl5ESKF5VRNpmVcYmmOZO67mOEESly8pnCz/c5vwj73HR0ryD5PzDIKc59NSjwf4wUJmAXi0smxledl98xwdIx85hfocvcsk11Mb+TahbBrqdmmlZ13NscOdRV8OBjaAuYVvBzPKmJlFHxJAzY2VCuaBOVVMkAEsy/BckOfWggU3VsuZ2eXV6LH+7nfn5u59snXVoo9Ov/nNX1B3QFVByeOpKCnPeUq2nXtuZ+JA5q3IkZerTp2/bHTtvnCyud3z+PEF8uHt4fXHn9ny8uuf7OHf+/CPn6xn/Yn926t3/Pn3xUdOlB/9fc5Dgz+ef3vjwKUXq2vPhcIz2/c2LD67vlpY0fRbpE7urFkadp7fMiu7btaJp9csmX868P2DnyWuBH7dd+3r79jKpd9WXT+y9ON1/9T2vHb1g2WXt72zhha2XBOG6m3BeUo6tTgX//zg1esi2HPmwuwr4g+vtp08Mnj22s/G1qGdQ52xqrpFIEbX1r9/qHPDmZrVvr2De+xL2S+sg/teqtl1ILfswOZjX+E3jr7Stbv2IjX/yyhzdl7t9he0rfsTWH944S99+4Y2HxrKde+6Oly+fwGYbKaj0xEAAA==","expires_in":7200,"refresh_token":"v^1.1#i^1#I^3#p^3#r^1#f^0#t^Ul4xMF81OjFCQ0RFQzIwMDE1QTZBN0U3RTFEQzU0NjBEN0ZEQTlEXzJfMSNFXjI2MA==","refresh_token_expires_in":47304000,"token_type":"User Access Token"}


    if token:
        # t_data = json.loads( token.text )
        tok = t_data['access_token']
        url_api = ' https://api.ebay.com/sell/inventory/v1/inventory_item'
        auth = 'Bearer ' + tok
        headers = { 'Authorization': auth }
        payload = {'offset': 0, 'limit': 2 }
        inventory = requests.get(url, headers=headers, params=payload)
        return '<h1>primi due oggetti dell inventario:<br>{}</h1>'.format(inventory.text)

    return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url)


    # if token:
    #     return '<h1>TOKEN RICEVUTO</h1>'
    # return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url)
