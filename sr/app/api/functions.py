from flask import jsonify, request, g, url_for, current_app, abort
from .. import db
from ..models import Store, User, Ecommerce
from . import api
import requests, os



@api.route('/get_report/<id_store>')
def get_report_store(id_store):

    store = Store.query.filter_by(id=id_store).first()

    if store is None:
        abort(404)

    refresh_token = store.oauth_json;


    # AGGIORNAMENTO TOKEN

    resp = requests.post(
                url="https://salesreporter.ddns.net/middle/ebay/refresh_token",
                data={'refresh_token': refresh_token}
                )

    ref_tok = resp.json()['access_token']
    mktp = Ecommerce.query.filter_by(id=self.ecommerce_id).first().name
    start_date = request.args['start_date']
    end_date =request.args['end_date']

    url = 'https://salesreporter.ddns.net/middle/ebay/get_report'
    headers = {
        'token': ref_tok
    }

    payload = {
        'marketplace':mktp,
        'start_date':start_date,
        'end_date':end_date
    }

    r = requests.get(url, headers=headers, params=payload)

    return jsonify( report=r.json() )
