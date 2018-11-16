from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Required, Email, Regexp, EqualTo
from ..models import User, Store


# class StoreForm(FlaskForm):
#     store_name = StringField('', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField( 'Email/Username', validators=[ Required(), Length(1,64)])

    password = PasswordField('Password', validators=[Required()] )
    # remember_me = BooleanField( 'Keep me logged in' )
    submit = SubmitField('LOG IN')




class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[
                                        Required(), Length(1,64),
                                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                'Usernames must have only letters, '
                                                'numbers, dots or underscores'
                                                )
                                        ]
                            )

    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')
