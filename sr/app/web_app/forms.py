from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired, Length, Required, Email, Regexp
from models import User, Store


class StoreForm(FlaskForm):
    store_name = StringField('', validators=[DataRequired()])
    
