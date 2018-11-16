from . import web_app
import requests
from flask import url_for, redirect, render_template



# 
# @web_app.route('/')
# def index():
#     return render_template
#
#






# @web_app.route('/prova_web')
# def prova_web():
#     r = requests.get(url_for('api.get_users', _external=True) )
#     return '</h1>ritorno dell api--></h1><br>' + str(r.text)
