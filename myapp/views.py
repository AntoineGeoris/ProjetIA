import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, request, jsonify, request
from flask.helpers import url_for
from wtforms.validators import Email
from myapp.forms import (RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm)
from myapp import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import myapp.models as models

@app.route('/')
@app.route('/index/')
def index() :
	return render_template('index.html', title = 'Accueil')

@app.route('/game/')
@login_required
def game() : 
	return render_template('game.html', title = 'Jeu')

@app.route('/game/new/', methods=['POST'])
def new_game():
	player = models.Player.query.filter_by(id=current_user.id).first()
	game = models.GameBoard(player=player.id)
	game.add_game_to_db()
	if game.active_player == 2:
		game.play()

	return jsonify(
		gameID = game.id,
		player1 = game.player_1_id,
		player1_pos = game.player_1_pos,
		player2_pos = game.player_2_pos,
		turn_no = game.no_turn,
		active_player = game.active_player,
		board = game.game_board_state_from_str()
	)

@app.route('/game/move/', methods=['POST'])
def game_move():
	game_state = request.get_json()
	game = models.GameBoard.query.filter_by(id = game_state.get('gameID')).first()
	if game.move_allowed(game_state.get('move'), game.active_player):
		game.play(game_state.get('move'))
		game.play()
	return jsonify(
		turn_no = game.no_turn,
		board = game.game_board_state_from_str(),
		player1_pos = game.player_1_pos,
		player2_pos = game.player_2_pos,
		activePlayer = game.active_player,
		player1_score = game.score('1'),
		player2_score = game.score('2'),
		is_gameover = game.is_gameover(),
	)

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit() :
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #decode used to obtain a string rather than a binary, easier for our planned db
		user = models.Player(username=form.username.data, email=form.email.data, password = hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Compte crée pour {form.username.data} ! Vous pouvez désormais vous connecter', 'success')
		return redirect(url_for('login'))
	return render_template('registration.html', title = 'Créer un compte', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit() :
		player = models.Player.query.filter_by(email=form.email.data).first()
		if player and bcrypt.check_password_hash(player.password, form.password.data):
			login_user(player, remember=form.remember.data)
			next_page = request.args.get('next') # Get the page that the user was trying to access before getting to loggin and get it if it exist, get none if none
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else :
			flash('L\'authentification a échoué, verifiez vos identifiants', 'danger')
	return render_template('login.html', title = 'Se connecter', form = form)

@app.route('/logout/')
def logout():
	logout_user()
	return redirect(url_for('index'))


def save_picture(form_picture) :
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename) # _ is used to not retain the first value (not used)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #Full path to the static/profile_pics/image_name.ext
	# Resizing image
	output_size = (125,125)	
	img = Image.open(form_picture)
	img.thumbnail(output_size)
	img.save(picture_path)
	return picture_fn


@app.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit() :
		if form.picture.data :
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Les informations du compte ont été mises à jour ! ', 'success')
		return redirect(url_for('account')) # Applying PRG (Post/Redirect/Get) design pattern
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title = 'Compte', image_file = image_file, form = form)

def send_reset_email(user):
	token = models.Player.get_reset_token(user)
	msg = Message('Projet-IA-Maki : Réinitialisation du mot de passe', 
					sender = "proj.ai.maki@gmail.com", 
					recipients=[user.email])
					#_external = True to obtain an absolute URL and not a relative one
	msg.body = f''' Pour réinitialiser votre mot de passe, cliquez sur le lien suivant :  
{url_for('reset_token', token=token, _external = True)} 

Si vous n'êtes pas à l'origine de cette requête, ignorez cet email et aucun changement ne sera apporté.
'''
	mail.send(msg)

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_request() :
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RequestResetForm()
	if form.validate_on_submit():
		player = models.Player.query.filter_by(email=form.email.data).first()
		send_reset_email(player)
		flash('Un email a été envoyé avec les instructions pour la réinitilisation du mot de passe', 'success')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title = "Réinitilisation mot de passe", form = form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token) :
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		player = models.Player.verify_reset_token(token)
		if not player :
			flash('Ce lien est expiré ou invalide', 'warning')
			return redirect(url_for('reset_request'))
		form = ResetPasswordForm()
		if form.validate_on_submit() :
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
			player.password = hashed_password
			db.session.commit()
			flash('Votre mot de passe a été modifié !', 'success')
			return redirect(url_for('login'))
		return render_template('reset_token.html', title = "Réinitilisation mot de passe", form = form)
  
@app.errorhandler(404)
def error_404(error):
	return render_template('error404.html'), 404	#404 = status code

@app.errorhandler(500)
def error_500(error):
	return render_template('error500.html'), 500