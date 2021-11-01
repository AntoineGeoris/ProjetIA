from sqlalchemy.orm import backref
from myapp import db
from datetime import datetime
import logging as lg

def init_db() :
	db.drop_all()
	db.create_all()
	db.session.commit()
	lg.warning('Database initialized !') 

	#Will probably have changes in the DB implementation, testing purpose

class GameBoard(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	player_1_pos = db.Column(db.String(2), nullable = False)
	player_2_pos = db.Column(db.String(2), nullable = False)
	date_played = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	no_turn = db.Column(db.Integer, nullable = False, default = 1)
	cells = db.Column(db.String(25), nullable = False, default = "1000000000000000000000002")

	player_1_id = db.Column(db.Integer, db.ForeignKey('player.id'))
	player_1 = db.relationship('Player', backref = db.backref('player_1'))
	player_2_id = db.Column(db.Integer, db.ForeignKey('player.id'))
	player_2 = db.relationship('Player', backref = db.backref('player_2'))

	def __init__(self, player_1 = None, player_2 = None):
		self.player_1 = player_1
		self.player_2 = player_2
		self.player_1_pos = "00"
		self.player_2_pos = "44"
		self.no_turn = 1
		self.cells = [
				[1,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,2]
			]

class Player(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique = True, nullable = False)
	username = db.Column(db.String(30), unique = True, nullable = False)
	password = db.Column(db.String(20), nullable = False)
	#image_file = db.Column(db.String(30), nullable = False)

	def __init__(self, email, username, password):
		self.email = email
		self.username = username
		self.password = password

	def __repr__(self):
		return f"User : ('{self.id}') '{self.username}'"