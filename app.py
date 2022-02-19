from flask import Flask, g, render_template, flash, url_for, redirect
from flask_login import LoginManager
import models
import forms

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = '49tfksadjfkpasbf--sdfsdf--//sdfsdf%sdfscsidjfSKMFSMDF'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ('login')


@app.before_request
def before_request():
    """ Conecta a la base de datos antes de cada Request"""
    g.db = models.DATABASE
    if g.db.is_closed():
        g.db.connect()


@app.after_request
def after_request(response):
    """ Cerramos conexion a la BBDD """

    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RefisterForm()
    if form.validate_on_submit():
        flash('Has sido registrado !! ', 'success')
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form = form)


@app.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None


if __name__ == '__main__':
    models.initialize()
    app.run(debug = DEBUG, host = HOST, port =PORT)