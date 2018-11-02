from werkzeug.security import generate_password_hash,  check_password_hash

from flask_login import UserMixin, AnonymousUserMixin

from . import db, login_manager # importato per poter registrare la funzione di
    # "load_user" che sostanzialmente ritorna lo user del db il cui id corrisponde
    # a quello passato in input sottoforma di stringa unicode(per questo castata ad intero),
    # sempre che la query dello stesso nel db abbia prodotto un risultato

# necessario per la generazione del token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column( db.String(64), unique=True, index=True )
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash =  db.Column( db.String(128) )

    # confirmed = db.Column(db.Boolean, default=False) # confermato?

    # relazione 1:N
    stores = db.relationship('Store', backref='users', lazy='dynamic')

    # METODI
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'stores_url': url_for('api.get_user_stores', id=self.id )
        }
        return json_user

    def __repr__(self):
        return '<User {}>'.format(self.username)

#----------------------------------------------------------


#----------------------------------------------------------
class Ecommerce(db.Model):
    __tablename__ = 'ecommerces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # dev_cred = db.Column(db.JSON)
    # RELAZIONI
    stores = db.relationship('Store', backref='ecommerces', lazy='dynamic')
    functions = db.relationship('Function', backref='ecommerces', lazy='dynamic')

    # METODI


    def to_json(self):
        json_ecommerce = {
            'url': url_for('api.get_ecommerces', id=self.id),
            'ecommerce_name': self.name,
            'functions_url': url_for('api.get_ecommerce_functions', id=self.id)

        }
        return json_ecommerce




    @staticmethod
    def insert_all():
        configured_ecom = ['EBAY_DE', 'EBAY_GB']

        for e in configured_ecom:
            ecom = Ecommerce.query.filter_by(name=e).first()
            if ecom is None: #se l'ecommerce non e' stato gia' inserito
                ecom = Ecommerce(name=e)
                db.session.add(ecom)

        db.session.commit()
        print('Ecommerce correctly entered!')


    def __repr__(self):
        return '<Ecommerce {}>'.format(self.name)

#----------------------------------------------------------

#----------------------------------------------------------
class Function(db.Model):
    __tablename__ = 'functions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    oauth_json = db.Column( db.String(4096) )
    # relazione N:1
    ecommerce_id = db.Column(db.Integer, db.ForeignKey('ecommerces.id') )


    # METODI
    @staticmethod
    def insert_all():
        configured_fun = [
            {
                'name':'ebay_get_report',
                'ecom': 'EBAY_DE'
            }
        ]

        for f in configured_fun:
            fun = Function.query.filter_by(name=f).first()
            if fun is None:
                ecom = Ecommerce.query.filter_by(name=f.ecom)
                fun = Function(name=f.name, ecommerce_id=ecom.id )
                db.session.add(fun)

        db.session.commit()
        print('functions correctly entered!')


    def __repr__(self):
        return '<Function {}>'.format(self.name)

#----------------------------------------------------------



#----------------------------------------------------------

class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(64))

    oauth_info = db.Column(db.String(4096))


    # relazione N:1
    user_id = db.Column(db.Integer, db.ForeignKey('users.id') )
    # relazione N:1
    ecommerce_id = db.Column(db.Integer, db.ForeignKey('ecommerces.id') )

    def to_json(self):
        json_store = {
            'url': url_for('api.get_store', id=self.id),
            'store_name': self.store_name,
            'reference_ecommerce_url': url_for('api.get_ecommerces', id=self.ecommerce_id),
            'store_user_owner': url_for('api.get_users', id=self.user_id),
        }
        return json_store



    # METODI
    def __repr__(self):
        return '<Store account {}>'.format(self.account_name)


#----------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----------------------------------------------------------
class AnonymousUser(AnonymousUserMixin):
    def can(Self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser



#                   PARTE RESTANTE DI USER
#                             |
#                             |
#                             |
#                             |
#                             |
#                          .  |  .
#                            . .
#                             .
    #
    #
    # def generate_auth_token(token, expiration):
    #     s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    #     return s.dumps({'id': self.id})
    #
    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token)
    #     except:
    #         return None
    #
    #     return User.query.get(data['id'])
    #
    # def __repr__(self):
    #     return '<User {}>'.format( self.username )
    #
    #
    #


    #
    #
    #
    #
    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps( {'confirm': self.id} )
    #
    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token) # load lancia l'eccezione se e' passato troppo tempo
    #     except:
    #         return False
    #     if data.get('confirm') != self.id: #se il token nn corrisponde a quello giusto
    #         return False
    #     # se sei arrivato qui, allora la conferma dell'email e' andata a buon fine
    #     self.confirmed = True
    #     db.session.add(self)
    #     db.session.commit()
    #     return True
    #
    #
    #
    # def generate_reset_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'reset': self.id}).decode('utf-8')
    #
    #
    # @staticmethod
    # def reset_password(token, new_password):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     user = User.query.get(data.get('reset'))
    #     if user is None:
    #         return False
    #     user.password = new_password
    #     db.session.add(user)
    #     return True
    #
    #
