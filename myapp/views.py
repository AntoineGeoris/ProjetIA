from flask import render_template, flash, redirect, request
from flask.helpers import url_for
from myapp.forms import RegistrationForm, LoginForm
from myapp.models import GameBoard
from myapp import app

 #Generated w/ secrets.token_hex()

@app.route('/')
@app.route('/index/')
def index() :
	return render_template('index.html', title = 'Accueil')

@app.route('/game/', methods=['GET', 'POST'])
def game() : 
	if request.method == 'GET':
		return render_template('game.html', title = 'Jeu')

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
	form = RegistrationForm()
	if form.validate_on_submit() :
		flash(f'Compte crée pour {form.username.data} !', 'success')
		return redirect(url_for('index'))
	return render_template('registration.html', title = 'Créer un compte', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit() :
		pass
	return render_template('login.html', title = 'Se connecter', form = form)