from flask import render_template, flash, redirect, request, jsonify
from flask.helpers import url_for
from myapp.forms import RegistrationForm, LoginForm
from myapp import app
import myapp.models as models

 #Generated w/ secrets.token_hex()

@app.route('/')
@app.route('/index/')
def index() :
	return render_template('index.html', title = 'Accueil')

@app.route('/game/', methods=['POST', 'GET'])
def game() : 
	if request.method == 'GET':
		return render_template('game.html', title = 'Jeu')
	else:
		new_game = models.new_game()
		return jsonify(
			gameID = new_game.id,
			player1 = new_game.player_1_id,
			player2 = new_game.player_2_id,
			turn_no = new_game.no_turn,
			board = new_game.game_board_state_from_str()
		)

@app.route('/game/move/', methods=['POST'])
def game_move():
	val = request.get_json()
	

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