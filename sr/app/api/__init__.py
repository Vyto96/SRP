from flask import Blueprint, request, abort, url_for, redirect, session
import os
api = Blueprint('api', __name__)

from . import users, stores, ecommerces, functions

# @api.before_request
# def before_request():
#     api_key = os.environ.get('SR_API_KEY')
#     req_api_key = request.headers.get('api_key')
#     if  req_api_key is None or req_api_key != api_key:
#         return 'api_key not valid', 401
