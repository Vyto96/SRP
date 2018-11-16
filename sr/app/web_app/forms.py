from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, Length, Required, Email, Regexp
from ..models import User, Store


# class StoreForm(FlaskForm):
#     store_name = StringField('', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField( 'Email', validators=[ Required(), Length(1,64), Email() ])

    password = PasswordField('Password', validators=[Required()] )
    # remember_me = BooleanField( 'Keep me logged in' )
    submit = SubmitField('LOG IN')
