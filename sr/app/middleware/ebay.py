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
    data = request.data
    dataDict = json.loads(data)

    url = 'https://api.ebay.com/identity/v1/oauth2/token'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': os.environ.get('EBAY_B64_CREDENTIAL')
    }

    #BODY
    payload = {
                'grant_type': 'refresh_token',
                'refresh_token': dataDict['refresh_token'],
                'scope': os.environ.get('EBAY_SCOPE_LIST')
    }

    resp = json.loads( requests.post(url, data=payload, headers=headers).json() )

    return jsonify( resp['access_token'] )




# @middle.route('/ebay/')
# def hello():
#     tok = 'v^1.1#i^1#f^0#p^3#I^3#r^0#t^H4sIAAAAAAAAAOVYbWwTZRxft27y4jSiQbOQ0B0sEsi1z732ellLunVjFdjKOkAHOO7lue3c9a7ePV1XAdmGYYKI8QNRE9ERTHxJeDUYIcYIEhM0IiExkpCgRsUZoglqQIkR77pu6yYC2/jQxH1Z7nn+b7/f//d/+tyBnrLpC7c2bL1a7rqreKAH9BS7XMRMML2sdNE9JcUVpUUgz8A10DO/x91XMlhtCQktyTdDK2noFvR0JzTd4rOLQSxl6rwhWKrF60ICWjyS+Hh4+TKe9AI+aRrIkAwN80QjQUyAkhjwS36F5jiR9kN7VR+O2WIEMTZA0IABNEeREuNXCHvfslIwqltI0FEQIwHB4QTAyUALwfI04CngpSiyFfOsgqalGrpt4gVYKFsun/U182q9eamCZUET2UGwUDRcH28KRyN1jS3VvrxYoRwPcSSglDX2qdaQoWeVoKXgzdNYWWs+npIkaFmYLzSUYWxQPjxczCTKz1It+WkOioARWYmFDMHeESrrDTMhoJvX4ayoMq5kTXmoIxVlbsWozYb4BJRQ7qnRDhGNeJx/K1KCpioqNINYXU34sZXxumbME4/FTKNLlaHsICVokvGzfoIIYKGOTBKaTmqCyaUZipUjeVyeWkOXVYcyy9NooBpoO8LxzFB5zNhGTXqTGVaQU0++HTfMIMm1Oi0d6mEKdehOV2HCpsGTfbw1/8OCGJXAnZIEKzOA40hGViiakpXADSThzPqEZRFyOhOOxXxOLVAUMnhCMDshSmqCBHHJpjeVgKYq8xSjkBSnQFxmAwpOBxQFFxmZxQkFQgChKEoB7v+jDoRMVUwhOKKQ8RtZiEHMYZRXBYVHRifUW2wM2HjL7LGTk0W3FcQ6EEryPl86nfamKa9htvtIAAjfo8uXxaUOmBCwEVv11sa4mhWIZJ/Wtj2P7AKCWLetPzu53o6Fmuvqm+viDW0tTUvrGoe1O6ay0PjV/0Aal4wkjBmaKmUKCyJlyjHBRJk41DR7YUogLQdkIcBzZn0UohPDsoMISdXrKM4rGQmfIdhnlrPUlq3acztGPssmyTt0AtiRvSYUZEPXMpNxnoCPqnfZI2SYmckkHHGegI8gSUZKR5NJl3OdgIeS0hRV05xTYjIJ89wnUqYuaBmkStZIyikJP5xMRhOJFBJEDUblQpiAvAEHJBNgpwyvwFB1qcgWtWrgSWfW7R9FAY81R3AqQDGcn+RoXGBl1s9K0pSAL29XCww3wRB2Q1mK5QDgpoQtArsKramUSAEO+GWcgjCA01BicIEOkDgjMAoElMiQHDMlzLWaap8ThXfPaDAsBOWpQbOvw4UFypnH4XGUWMa+L0Io4bSssLhISwROkcRtdzO34KZvcLP81yuFb+wbfago+0f0uY6APtehYpcL+EAVMQ9UlpWsdJfcXWGpCHrtW6jXUtt1+0XVhN5OmEkKqllc5loz5+DbbXnfEAbWgYdGviJMLyFm5n1SAHNGd0qJex8sJzgCkAGCpQEFWsG80V03Mdv9gDbrwu/q1ir/rpodoeqGytkLDw72gvIRI5ertMjd5yqaUXO/tfnwMxf3nv^1.1#i^1#r^0#I^3#f^0#p^3#t^H4sIAAAAAAAAAOVYW2wUVRjudtuSirWBcNHKwzIgQcnsnpnZmd2ZsAtLL+kCbZduQShoc2bmTDswO7PMnG274aVpAiEhoGBQTIwpRLlGQARi0Bei8QEVId5CYhQ0IUYDjYHEiFE8s71tKwJtedjEzSab85//9n3//589M6CnrPy5bfXbfq/wTCnu6wE9xR4PMxWUl5UuesJbXFVaBPIUPH0983tKer0/L3ZgykhLzchJW6aDfN0pw3SknDBCZWxTsqCjO5IJU8iRsCIlYw0rJdYPpLRtYUuxDMoXr4lQUOUBBAhxISAIWoghUnPIZ4sVoUSOFYJBAcoyEkVGkMm+42RQ3HQwNHGEYgETphlAs2ILw0u8KPEhPxBCrZRvDbId3TKJih9Q0Vy6Us7Wzsv1/qlCx0E2Jk6oaDxWl2yKxWtqG1sWB/J8RQd5SGKIM87oVbWlIt8aaGTQ/cM4OW0pmVEU5DhUIDoQYbRTKTaUzATSz1HNcBDySBOhHOYI1fCRUFln2SmI75+HK9FVWsupSsjEOs4+iFHChrwRKXhw1UhcxGt87s+qDDR0TUd2hKpdFlu3OlnbTPmSiYRtdeoqUnNIgywfEkIMI1LRjmwa2W5ohh8MM+BrkOQxcaotU9Vdyhxfo4WXIWKIxjITzGOGKDWZTXZMw24++XqhYQb5VrekAzXM4A7TrSpKERp8ueWD+R9qiJEWeFQtwctBXtDC5BsKyyy8V0u4sz7utoi6lYklEgE3FyTDLJ2C9iaE0wZUEK0QejMpZOuqxPEay4U1RKuCqNFBUdNomVcFmtEQIqeCLCti+P/THRjbupzBaLhDxm7kIEYol1FJh5qErU3IbCEYqLGauWNnsC26nQjVgXFaCgS6urr8XZzfstsDLABMYG3DyqTSgVKk8kO6+oOVaT3XIAoiVo4uYZJAhOom/UeCm+1UtLm2rrk2Wd/W0rSitnGod0dlFh0r/Q+kScVKo4Rl6Eq2sCBytpqANs4mkWEQwaRAOi7IQoDnzvoIRNeHQ5zAtO53O86vWKmABcmZ5Yracln7HkYp4BCS/AMnAPHstxFULdPITsR4HDa62UlGyLKzEwk4bDwOG6goVsbEEwk3aDoOCy1jaLphuKfERALmmY8nTRMaWawrznDISTV+LJ2Op1IZDGUDxdVCmIC8AQcsLwqThldgqDp1TJpat+i0O+vkTxHSieYamhM5Phxiw0EaCqoQEhRlUsAb2vUCw83wDCmowAlhAMKTwlaDOgutqJzMgTAIqTSHkEgHkcLTMCiyNA95DQFO5tkwPynM1YZOzonCu2fUWw5G6uSgketwYYFy53FoHBWBJ/dFhBQ6qGoCLQcVhuZY5qGrOSgoCd7jZvmvR4rA6Cf6aFHuw/R6zoBez7vFHg8IgGeYeWBumXd1iffxKkfHyE9uoX5HbzfJg6qN/JtQNg11u7jMs37OySNtee8Q+l4ATw6/RSj3MlPzXimAOSM7pUzl7AomzABWZHhe5EOtYN7Ibgkzq2TGfOfX6sPltcEl33/8Rv2B6YvpC+YuUDGs5PGUFpX0eopmb9h77Owfvc9v2Vbk7Kyc3fX3hvOfVuxfoL8aO3m856v9h6c93R36fNq03y7tmvLs8rZvV23Vp79+94PXbrWGlxyg++Z473BfR68e+qShvsrYe4d9+5sdh42ru2ferrx9+dJxfsF155eP8FpPU/M+VlzwGV6623uuvu6Lv95j3zzRtGd/38ET1/dFnrq24seLO0o8X66DG26fWfj+mrmXZwq31M17D1WdPX/qSnbPy6ny1vUHt9wU+r0v3ujeGPS9dWHrtf5972y3b/60Q6du3Phu8w/ZPz0n+s/NWuFbPmM73V8ZB5u9RxbtOs2ApRVX51/ZE7646KVbp88d2bmq49grp+iN1NzHoguPHr27+sOB8v0D5gwpOt0RAAA='
#
#     url = 'https://salesreporter.ddns.net/middle/ebay/get_report'
#     headers = {
#         'token': tok
#     }
#     payload = {
#         'marketplace':'EBAY_DE',
#         'start_date':'20181020',
#         'end_date':'20181029'
#     }
#
#     r = requests.get(url, headers=headers, params=payload)
#
#     return jsonify( r.json() )

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
