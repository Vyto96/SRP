from flask import url_for, redirect, render_template, flash
from . import web_app
from .forms import LoginForm, RegistrationForm
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
            # spa_link = os.environ.get('SR_SPA')
            spa_link = '/fuffa'
            # + my_form.email.data  + '/'# + r.json()['id']
            # spa_link += '/' + my_form.email.data  + '/'
            return redirect(spa_link)

        flash('invalid username or password, sorry!')
    return render_template('login.html', form=my_form)


@web_app.route('/register', methods=['GET', 'POST'])
def register():
    my_form = RegistrationForm()
    if my_form.validate_on_submit():

        url = url_for('api.register',  _external=True)
        headers = {
            'api_key': os.environ.get('SR_API_KEY'),
        }

        payload = {
            'email': my_form.email.data,
            'username': my_form.username.data,
            'password': my_form.password.data
        }

        r = requests.post(url, data=payload, headers=headers)


        if r.status_code == 200:
            flash(r.text)
            return redirect(url_for('web_app.login'))
        flash(r.text)
    return render_template('register.html', form=my_form)











# @web_app.route('/prova_web')
# def prova_web():
#     r = requests.get(url_for('api.get_users', _external=True) )
#     return '</h1>ritorno dell api--></h1><br>' + str(r.text)
