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

@app.route('/game/')
def game() : 
	return render_template('game.html', title = 'Jeu')

@app.route('/game/new/', methods=['POST'])
def new_game():
	playersID = request.get_json()
	game = models.new_game(player1=playersID.get('player1ID'), player2=playersID.get('player2ID'))
	return jsonify(
		gameID = game.id,
		player1 = game.player_1_id,
		player2 = game.player_2_id,
		turn_no = game.no_turn,
		active_player = game.active_player,
		board = game.game_board_state_from_str()
	)

@app.route('/game/move/', methods=['POST'])
def game_move():
	game_state = request.get_json()
	game = models.GameBoard.query.filter_by(id = game_state.get('gameID')).first()
	game.play(game_state.get('move'))
	models.db.session.commit()
	return jsonify(
		turn_no = game.no_turn,
		board = game.game_board_state_from_str(),
		activePlayer = game.player_2_id,
	)

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