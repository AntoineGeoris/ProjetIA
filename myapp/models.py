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
	board_state = db.Column(db.String(25), nullable = False, default = "1000000000000000000000002")

	player_1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)
	player_2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)

	__game_board_state_to_str = lambda cells : "" if len(cells) == 0 else "".join(cells[0]) + __game_board_state_to_str(cells[1:])

	def game_board_state_from_str(self):
		board = []
		for i in range(1,6):
			line = []
			for y in range((i - 1) * 5, i * 5):
				line.append(self.board_state[y])
			board.append(line)
		return board

	def move_allowed(self, game_state, player_pos, move):
		line = player_pos[0]
		column = player_pos[1]

		if move == "left":
			return column - 1 >= 0 and game_state[line][column - 1] == '0'
		if move == "right":
			return column + 1 >= 0 and game_state[line][column + 1] == '0'
		if move == "down":
			return line + 1 >= 0 and game_state[line + 1][column] == '0'
		
		return line - 1 >= 0 and game_state[line - 1][column] == '0'

	def move(self, player_pos, move):
		board_state = self.__game_board_state_from_str()

		if self.move_allowed(board_state, player_pos, move):
			line = player_pos[0]
			column = player_pos[1]

			if move == "left":
				board_state[line][column - 1] = board_state
				player_pos[1] = str(int(column) - 1)
			elif move == "right":
				board_state[line][column + 1] = board_state
				player_pos[1] = str(int(column) + 1)
			elif move == "down":
				board_state[line + 1][column] = board_state
				player_pos[0] = str(int(line) + 1)
			else:
				board_state[line - 1][column] = board_state
				player_pos[0] = str(int(line) - 1)

			self.board_state = self.__game_board_state_to_str(board_state)


class Player(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique = True, nullable = False)
	username = db.Column(db.String(30), unique = True, nullable = False)
	password = db.Column(db.String(20), nullable = False)
	#image_file = db.Column(db.String(30), nullable = False)

	#games = db.relationship('GamBoard', backref = db.backref('player') , lazy = True)

	def __repr__(self):
		return f"User : ({self.id}) {self.username}"


def new_game(player1 = None, player2 = None):
	new_game = GameBoard(player_1_id = player1, player_2_id = player2)
	db.session.add(new_game)
	db.session.commit()
	return new_game