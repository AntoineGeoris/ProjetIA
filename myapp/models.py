from flask_sqlalchemy import SQLAlchemy
from .views import app
from datetime import datetime
import logging as lg

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

def init_db() :
	db.drop_all()
	db.create_all()
	db.session.commit()
	lg.warning('Database initialized !') 

	#Will probably have changes in the DB implementation, testing purpose

class Player(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(80), unique = True, nullable = False)
	image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
	password =  db.Column(db.String(60), nullable = False)
	games = db.relationship('Game', backref='Participant')
	moves = db.relationship('Move', backref='Initiator')

	def __repr__(self) :
		return f"User('{self.username}, {self.email}, {self.image_file}')"

class Move(db.Model):	
	x_move = db.Column(db.Integer, primary_key = True)
	y_move = db.Column(db.Integer, primary_key = True)
	no_turn = db.Column(db.Integer, primary_key = True)
	player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = False)
	game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable = False)


class Game(db.Model):	
	id = db.Column(db.Integer, primary_key = True)
	id_winner = db.Column(db.Integer, nullable = True)
	date_played = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) #no parenthesis, we want to pass the function as an argument, not having the current time (when 'executed') 
	player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = False)
	moves = db.relationship('Move', backref='Initiator')

	def __repr__(self) :
		return f"Game('{self.id}, {self.id_winner}, {self.date_played}')"