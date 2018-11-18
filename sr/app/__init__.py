from flask import Flask
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_cors import CORS
from flask_bootstrap import Bootstrap
#
#
# # from flask_pagedown import PageDown
# from flask_moment import Moment
##
# mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
cors = CORS()
#
# pagedown = PageDown()
# moment = Moment()
#
login_manager.login_message = 'Warning: login to view this page'
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)
    config.init_app(app)
#     mail.init_app(app)
    db.init_app(app)


    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    bootstrap.init_app(app)
    cors.init_app(app)
#     pagedown.init_app(app)
#     moment.init_app(app)

#test route
    @app.route('/')
    def index():
        return '<h1>hello from sales reporter </h1>'

# #-------BLUEPRINT REGISTRATION
    from .api import api as api_BP
    app.register_blueprint(api_BP, url_prefix='/api')

    from .web_app import web_app as web_app_BP
    app.register_blueprint(web_app_BP, url_prefix='/web_app')

    from .middleware import middle as middle_BP
    app.register_blueprint(middle_BP, url_prefix='/middle')

    return app
