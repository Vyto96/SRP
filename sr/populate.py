from sr import app
from app import db
from app.models import User, Store, Ecommerce, Function

Ecommerce.insert_all()
Function.insert_all()
