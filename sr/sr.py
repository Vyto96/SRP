import os
from app import create_app, db
from app.models import User, Store, Ecommerce, Function


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=True)
