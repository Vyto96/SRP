from flask import url_for, redirect, render_template, flash
from . import web_app
from .forms import LoginForm
import requests, os




@web_app.route('/')
def index():
    return redirect( url_for('web_app.login') )


@web_app.route('/login', methods=['GET', 'POST'])
def login():

    my_form = LoginForm()

    if my_form.validate_on_submit():

        url = url_for('api.try_login',  _external=True)

        headers = {
            'api_key': os.environ.get('SR_API_KEY'),
            'logger': my_form.email.data,
            'psw': my_form.password.data
        }

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return redirect( os.environ.get('SR_SPA'))

        flash('invalid username or password, sorry!')
    return render_template('login.html', form=my_form)


@web_app.route('/register', methods=['GET', 'POST'])
def register():
return '<h1>REGISTER PAGE </h1>'    

# @web_app.route('/prova_web')
# def prova_web():
#     r = requests.get(url_for('api.get_users', _external=True) )
#     return '</h1>ritorno dell api--></h1><br>' + str(r.text)
