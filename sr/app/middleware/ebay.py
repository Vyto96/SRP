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

    token =  {
    "access_token": "v^1.1#i^1#I^3#f^0#p^3#r^0#t^H4sIAAAAAAAAAOVYW2wUVRju9qYEqxgrEKjJOhRQZHbPXHd30l3dtltboe2yW5Cr9czMmXZgdmaZOdt2iWJZCcEL0YBoiCRUJEZADT70RRN9AGPA8OIl8QXFBLThovFFwJjgmW27bGu4tOWhifOymf/8t+/7///sOQP6K2cs2dG840qV557SgX7QX+rxMDPBjMqKJ+4vK51XUQKKFDwD/bX95bmyoToHpoy0lEBO2jId5O1LGaYj5YVhKmObkgUd3ZFMmEKOhBUpGW1dLrE+IKVtC1uKZVDelsYwxUOVgzxSGE0MCDIXIFJz1GeHFaZUBDWGRSrLhpDMhCBZd5wMajEdDE0cpljABGkG0CzbwfASF5R4zsewwlrKuwrZjm6ZRMUHqEg+XSlvaxfleutUoeMgGxMnVKQl2pRsj7Y0xto66vxFviIjPCQxxBln7FuDpSLvKmhk0K3DOHltKZlRFOQ4lD8yHGGsUyk6mswk0s9TLXOI01CIF0RWFslzV6hssuwUxLfOw5XoKq3lVSVkYh1nb8coYUPeiBQ88tZGXLQ0et2fFRlo6JqO7DAVq4+uWZmMJShvMh63rR5dRaqLlOFZwIMQG2CpSE8WWyFxJMKwmxF+x4VosExVd9lyvG0WrkckXTSeFLaIFKLUbrbbUQ27qRTriQXymLVuNYfLl8HdpltQlCIMePOvt6d+tBduVP9udYPCiJys8AIfRLwmo5sOljvrE+mIiFuUaDzud3NBMszSKWhvQjhtQAXRCqE3k0K2rkqcoLFcUEO0KoY0mg9pGi0LqkgzGkIAIVlWQsH/RWNgbOtyBqNCc4xfyKMLUy6Zkg41CVubkNmRTSNqvGZ+sxnpiD4nTHVjnJb8/t7eXl8v57PsLj8LAONf3bo8qXSjFCn6qK5+e2Vaz/eGgoiVo0uYJBCm+kjrkeBmFxVJxJoSsWRzZ0f7sljbaNuOySwyXnoTpEnFSqO4ZehKdnpB5Gw1Dm2cTSLDIIIpgXRckNMLnjvrrg+HOIFp3ed2nE+xUn4Lku3KFXXms/beiZLfIST5hoefePfZCKqWaWQnYzwBG93sISNk2dnJBCwYT8AGKoqVMfFkwo2YTsBCyxiabhjuLjGZgEXmE0nThEYW64pTCDmlxo+m0y2pVAZD2UAt6vSaAA6wQuFPYfLwphmqHh2TptYtmpy9eyAdTzTSnDvrIU4IBtggT0NRFQOiokwJeGuXPs1wMwIQQwzDgRAA7JSwNaKe6VZUTuZAEARUmkMoRJMrlEBDPsTSAhQ0BDhZYIPClDA3GDrZJ6bfOaPZcjBSpwaNnISnFyh3JkfHUREFcl5ESKF5VRNpmVcYmmOZO67mOEESly8pnCz/c5vwj73HR0ryD5PzDIKc59NSjwf4wUJmAXi0smxledl98xwdIx85hfocvcsk11Mb+TahbBrqdmmlZ13NscOdRV8OBjaAuYVvBzPKmJlFHxJAzY2VCuaBOVVMkAEsy/BckOfWggU3VsuZ2eXV6LH+7nfn5u59snXVoo9Ov/nNX1B3QFVByeOpKCnPeUq2nXtuZ+JA5q3IkZerTp2/bHTtvnCyud3z+PEF8uHt4fXHn9ny8uuf7OHf+/CPn6xn/Yn926t3/Pn3xUdOlB/9fc5Dgz+ef3vjwKUXq2vPhcIz2/c2LD67vlpY0fRbpE7urFkadp7fMiu7btaJp9csmX868P2DnyWuBH7dd+3r79jKpd9WXT+y9ON1/9T2vHb1g2WXt72zhha2XBOG6m3BeUo6tTgX//zg1esi2HPmwuwr4g+vtp08Mnj22s/G1qGdQ52xqrpFIEbX1r9/qHPDmZrVvr2De+xL2S+sg/teqtl1ILfswOZjX+E3jr7Stbv2IjX/yyhzdl7t9he0rfsTWH944S99+4Y2HxrKde+6Oly+fwGYbKaj0xEAAA==",
    "expires_in": 7200,
    "refresh_token": "v^1.1#i^1#I^3#p^3#r^1#f^0#t^Ul4xMF81OjFCQ0RFQzIwMDE1QTZBN0U3RTFEQzU0NjBEN0ZEQTlEXzJfMSNFXjI2MA==",
    "refresh_token_expires_in": 47304000,
    "token_type": "User Access Token"}


    token2 = {
    "access_token":"v^1.1#i^1#p^3#r^0#I^3#f^0#t^H4sIAAAAAAAAAOVYW2wUVRju9mYaQNSgKKIuAyVAM7tnZnZmZ0d26dJLukjbtVsIFqTM5Uw7dHZmM+dM233AlG0gEI0EY3yuMSYSvKBCNGBATUyAKIkiCC9gVBJMjBiJoGKMZ7a3bUWgLQ+b2Jdmzvlv3/d//9kzAwYqq1bsbNp5fY7vntKhATBQ6vMxs0BVZUXNvWWlCypKQIGBb2hgyUB5ruzySiSnzYzUBlHGthD096dNC0n5xSjlOpZky8hAkiWnIZKwKqXizWslNgCkjGNjW7VNyp+oj1JhgdUiHKdzmq6oAieSVWs0ZrsdpSIio0CODylhjleEEE/2EXJhwkJYtnCUYgEj0gygWbad4SU2InFiQBSEDsq/HjrIsC1iEgBULF+ulPd1Cmq9dakyQtDBJAgVS8QbU63xRH1DS/vKYEGs2AgPKSxjF018qrM16F8vmy68dRqUt5ZSrqpChKhgbDjDxKBSfLSYaZQ/TDUTDoU5KIhA1oCqw7tCZaPtpGV86zq8FUOj9bypBC1s4OztGCVsKFuhikeeWkiIRL3f+/e0K5uGbkAnSjWsjj+zLtXQRvlTyaRj9xoa1DykTIjlw0KYYSJUrDubgY6XmuFH0gzHGiF5Up4629IMjzLkb7Hxakgc4WRmmAJmiFGr1erEdezVU2gXHmOQ6fBaOtxDF3dbXldhmtDgzz/env9RQYxL4G5JQmCBGlYYJQRgiJehdhNJeLM+ZVnEvM7Ek8mgVwtU5Cydlp0eiDOmrEJaJfS6aegYmsTxOsuJOqQ1IaLToYiu0wqvCTSjQwggVBQ1Iv5/1IGxYyguhmMKmbyRhxilPEYlQ9YlbPdAq51goCZb5o+dEVn0oyjVjXFGCgb7+voCfVzAdrqCLABMcEPz2pTaDdMyNWZr3N6YNvICUckRQuwlTAqIUv1EfyS51UXF2hoa2xpSTZ3trU81tIxqd0Jlscmr/4E0pdoZmLRNQ80WF0TO0ZKyg7MpaJpkYUYgkQeyGOB5sz4O0YuBSBA5YwQ8xQVUOx20ZXJmeUud+ar9d2IURISkwPAJQCIHHChrtmVmp+M8BR/D6iUjZDvZ6SQcc56Cj6yqtmvh6aQbcZ2Ch+6aumGa3ikxnYQF7lMp05LNLDZUNJZyRsKPZzKJdNrFsmLChFYME1Aw4IDlI8KM4RUZql4DE1EbNp3xZp38KMp0sq2e5iIcL4ZZMUTLgiaEBVWdEfDmLqPIcDM8QxoqcOTyC8QZYauHvcXWVE7hgAjCGs1BGKFDUOVpORRhaV7mdQg4hWdFfkaY60yDnBPFd89oshGG2sygketwcYHy5nF0HFWBJ/dFCFU6pOkCrYRUhuZY5o67ObJQHrrJzfJfrxTBiW/0sZL8H5PzHQI537ulPh8IgmpmMVhUWbauvGz2AmRgGCC30AAyuizyourAQA/MZmTDKa30bVx4YF9nwTeEoWfBw2NfEarKmFkFnxTAwvGdCmbu/DmMyACWwGQjnNgBFo/vljMPlc97eevF/o/Xn2g9d+HA6oORmvPtL31xBcwZM/L5KkrKc76SPY+fYn47fAyv2yKuWdG4qpOvRbF3Hpm79bjvZG2H27Xr7cpv/qpd8+nZ7rpvI9f/qF0xL1dCX11y4+ulbvbVJ5Y+CJ5b9tHl+VVOTQ/+6RqzfK6eu7EzFjhVdn5fa9+1B3LOi5s2Pb/2z7NNucMHrDN/J36uwPbBUu6+Mz9Q/t1nZuU++HL5lpLwoc3S+frBV1buGXxh44fiSRx+r+fRjqPNA09eeOP6xVXa9v2z2dfOvb57L9g4+Pulvorq6P1VRx9D39d175DSb+65uu3K6RMDg9XCfNdZ9OPxU7MXHT+9YVnN9qEbC7quLRcvNcHOX4aOVP/6Ofrus/37KhZW7Tjyfvatzd1fHdv1ybFtw+37BxfB/cvdEQAA",
    "expires_in":7200,
    "refresh_token":"v^1.1#i^1#I^3#r^1#f^0#p^3#t^Ul4xMF8xMTpFMDQyNEZENUM0MjFGMDI2RTdBRTI1RDI1MUZDMjAxRV8yXzEjRV4yNjA=",
    "refresh_token_expires_in":47304000,
    "token_type":"User Access Token"}



    if token:
        # t_data = json.loads( token.text )
        tok2 = token['access_token']
        url_api = 'https://api.ebay.com/sell/inventory/v1/inventory_item'
        auth = 'Bearer ' + tok2
        headers = { 'Authorization': auth }
        payload = {'offset': 0, 'limit': 2 }
        inventory = requests.get(url_api, headers=headers, params=payload)
        
        return '<h1>primi due oggetti dell inventario:<br>{}</h1>'.format(inventory.text)

    return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url)


    # if token:
    #     return '<h1>TOKEN RICEVUTO</h1>'
    # return '<h1>TOKEN NON RICEVUTO<br>URL:{}</h1>'.format(url)
