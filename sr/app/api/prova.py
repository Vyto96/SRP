from . import api
from flask import url_for, jsonify, request, json
import requests


@api.route('/prova_post', methods=['GET', 'POST'])
def prova_post():
    if request.method == 'POST':
        if request.is_json:
            j = json.loads( request.get_json() )
            j['k1'] ='valore1'
            j['k2'] ='valore2'
            return jsonify(j)
        else:# not a json body in post request
            return '<h1>non mi hai inviato un json </h1>'
    else:
        return '<h1> ciao antonio </h1> '


@api.route('/prova2')
def prova2():
    url = 'http://0.0.0.0:5000/api/prova_post'
    data = { 'k1':'val1', 'k2':'val2'}
    r = requests.post( url, json=json.dumps(data) )
    return jsonify( r.json() )
