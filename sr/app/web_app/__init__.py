from flask import Blueprint

web_app = Blueprint('web_app', __name__)

#import dei file .py che contengono le view fun che ritornano le risorse indicate dal nome del file stesso
from . import main_view
