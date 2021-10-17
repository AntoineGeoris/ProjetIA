from flask import Flask, render_template, flash, redirect
from flask.helpers import url_for
from .forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config.from_object('config')
app.config['SECRET_KEY'] = 'a33653a7074d917291e2b70c227fb065' #Generated w/ secrets.token_hex()

@app.route('/')
@app.route('/index/')
def index() :
	return render_template('index.html', title = 'Accueil')

@app.route('/game/')
def game() : 
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