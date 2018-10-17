from . import web_app
import requests
from flask import url_for, redirect

@web_app.route('/prova_web')
def index():
    r = requests.get(url_for('api.get_users', _external=True) )
    return '</h1>ritorno dell api--></h1><br>' + str(r.text)
