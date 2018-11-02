import os
from app import create_app, db
from app.models import User, Store, Ecommerce, Function


app = create_app()
Ecommerce.insert_all()
Function.insert_all()

if __name__ == '__main__':
    app.run(use_reloader=True, port=4000)
