from sqlalchemy.orm import backref
from myapp import db
from datetime import datetime
import logging as lg

def init_db() :
	db.drop_all()
	db.create_all()
	players = [
		Player(email = "natan@email.be", username = "Natan", password = "1235"),
		Player(email = "mathieu@email.be", username = "Mathieu", password = "1235"),
		Player(email = "antoine@email.be", username = "Antoine", password = "1235"),
	]
	db.session.add_all(players)
	db.session.commit()
	lg.warning('Database initialized !') 

	#Will probably have changes in the DB implementation, testing purpose

class GameBoard(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	player_1_pos = db.Column(db.String(2), nullable = False, default = "00")
	player_2_pos = db.Column(db.String(2), nullable = False, default = "44")
	date_played = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	no_turn = db.Column(db.Integer, nullable = False, default = "1")
	cells = db.Column(db.String(25), nullable = False, default = "1000000000000000000000002")

	player_1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)
	player_2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)


class Player(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique = True, nullable = False)
	username = db.Column(db.String(30), unique = True, nullable = False)
	password = db.Column(db.String(20), nullable = False)
	#image_file = db.Column(db.String(30), nullable = False)

	#games = db.relationship('GamBoard', backref = db.backref('player') , lazy = True)

	def __repr__(self):
		return f"User : ({self.id}) {self.username}"
