import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SR_SECRET_KEY') or 'hard to guess string'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SR_MAIL_SENDER = os.environ.get('SR_MAIL_SENDER')
    SR_ADMIN = os.environ.get('SR_ADMIN')

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # EBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or \
                            'sqlite:///' + os.path.join(basedir, 'salesreporter_DB.sqlite')


    @staticmethod
    def init_app(app):
        pass
