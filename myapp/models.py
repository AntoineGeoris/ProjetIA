from sqlalchemy.orm import backref, column_property
from myapp import db
from myapp.ia import AI
from datetime import datetime
from enum import IntEnum
import logging as lg
from random import choice
from statistics import mode

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

class GameType(IntEnum):
	AI_AGAINST_AI = 1
	PLAYER_AGAINST_AI = 2
	PLAYER_AGAINST_PLAYER = 3

	#Will probably have changes in the DB implementation, testing purpose

class GameBoard(db.Model):
	BOARD_HEIGHT = 5
	BOARD_WIDTH = 5

	id = db.Column(db.Integer, primary_key = True)
	player_1_pos = db.Column(db.String(2), nullable = False, default = "00")
	player_2_pos = db.Column(db.String(2), nullable = False, default = "44")
	date_played = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	no_turn = db.Column(db.Integer, nullable = False, default = "0")
	state = db.Column(db.String(25), nullable = False, default = "1000000000000000000000002")
	type = db.Column(db.Integer, nullable = False, default = GameType.PLAYER_AGAINST_AI)
	active_player = db.Column(db.Integer, nullable = True)

	player_1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)
	player_2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)

	def __game_board_state_to_str(self, board):
		string = ""
		for i in range(5):
			string += "".join(board[i])

		self.state = string

	def game_board_state_from_str(self):
		board = []
		for i in range(1,6):
			line = []
			for y in range((i - 1) * 5, i * 5):
				line.append(self.state[y])
			board.append(line)
		return board

	def pos_active_player(self):
		pass

	def move_allowed(self, move, line, column, board, num_player):
		if move == "right":
			return column + 1 < self.BOARD_HEIGHT and (board[line][column + 1] == '0' or board[line][column + 1] == str(num_player))
		if move == "left":
			return column - 1 >= 0 and (board[line][column - 1] == '0' or board[line][column - 1] == str(num_player))
		if move == "up":
			return line - 1 >= 0 and (board[line - 1][column] == '0' or board[line - 1][column] == str(num_player))
		
		return line + 1 < self.BOARD_HEIGHT and (board[line + 1][column] == '0' or board[line + 1][column] == str(num_player))

	def move(self, move, num_player, board, line, column):
		initialPos = str(line) + str(column)
		
		if move == "right":
			column += 1
		elif move == "left":
			column -= 1
		elif move == "up":
			line -= 1
		else:
			line += 1
		
		newPos = str(line) + str(column)
		board[line][column] = str(num_player)

		self.enclosure(board, initialPos, newPos, move, num_player)
		if num_player == 1:
			self.player_1_pos = str(line) + str(column)
		else:
			self.player_2_pos = str(line) + str(column)

		return board
			
	def enclosure(self, board, initialPos, newPos, move, num_player):
		if move in ("down", "up"):
			if not "0" in initialPos and not "4" in initialPos and ("0" in newPos or "4" in newPos):
				saveBoxes = []
				line = int(newPos[0])
				column = int(newPos[1])
				if num_player == 1:
					columnIncrement = -1
					columnLimit = lambda column : column >= 0
				else:
					columnIncrement = 1
					columnLimit = lambda column : column < self.BOARD_WIDTH
				
				if move == "up":
					lineIncrement = 1
					lineLimit = lambda line : line < self.BOARD_HEIGHT
				else:
					lineIncrement = -1
					lineLimit = lambda line : line >= 0

				while columnLimit(column + columnIncrement) and board[line][column + columnIncrement] == '0':
					column += columnIncrement
					saveBoxes.append(str(line) + str(column))
					while lineLimit(line + lineIncrement) and board[line + lineIncrement][column] == '0':
						saveBoxes.pop()						
						line += lineIncrement
						saveBoxes.append(str(line) + str(column))
						while columnLimit(column - columnIncrement) and board[line][column - columnIncrement] == '0':
							column += -(columnIncrement)
							saveBoxes.append(str(line) + str(column))

				for box in saveBoxes:
					line = int(box[0])
					column = int(box[1])
					if move == "up":
						while line >= 0:
							board[line][column] = str(num_player)
							line -= 1
					else:
						while line < self.BOARD_HEIGHT:
							board[line][column] = str(num_player)
							line += 1

		else:
			if not "0" in initialPos and not "4" in initialPos and ("0" in newPos or "4" in newPos):
				saveBoxes = []
				line = int(newPos[0])
				column = int(newPos[1])
				if num_player == 1:
					lineIncrement = -1
					lineLimit = lambda line : line >= 0
				else:
					lineIncrement = 1
					lineLimit = lambda line : line < self.BOARD_HEIGHT

				if move == "left":
					columnIncrement = 1
					columnLimit = lambda column : column < self.BOARD_HEIGHT
				else:
					columnIncrement = -1
					columnLimit = lambda column : column >= 0

				while lineLimit(line + lineIncrement) and board[line + lineIncrement][column] == '0':
					line += lineIncrement
					saveBoxes.append(str(line) + str(column))
					while columnLimit(column + columnIncrement) and board[line][column + columnIncrement] == '0':
						saveBoxes.pop()
						column += columnIncrement
						saveBoxes.append(str(line) + str(column))
						while lineLimit(line - lineIncrement) and board[line - lineIncrement][column] == '0':
							line += -(lineIncrement)
							saveBoxes.append(str(line) + str(column))
						

				for box in saveBoxes:
					line = int(box[0])
					column = int(box[1])
					if move == "left":
						while column >= 0:
							board[line][column] = str(num_player)
							column -= 1
					else:
						while column < self.BOARD_WIDTH:
							board[line][column] = str(num_player)
							column += 1
					

		return board
						

	def play(self, move):
		#moves = ["left", "up", "up","up", "up"]
		ia = AI()
		board = self.game_board_state_from_str()
		if self.type == GameType.PLAYER_AGAINST_AI:
			line = int(self.player_1_pos[0])
			column = int(self.player_1_pos[1])

			if self.move_allowed(move, line, column, board, 1):
				board = self.move(move, 1, board, line, column)

				move = ia.get_move()
				line = int(self.player_2_pos[0])
				column = int(self.player_2_pos[1])
				while not self.move_allowed(move, line, column, board, 2):
					move = ia.get_move()
				
				board = self.move(move, 2, board, line, column)

				""" for move in moves:
					line = int(self.player_2_pos[0])
					column = int(self.player_2_pos[1])
					board = self.move(move, 2, board, line, column) """

				print("Postion joueur 1 : ", self.player_1_pos)
				print("Postion joueur 2 : ", self.player_2_pos)

			self.no_turn += 2
			self.__game_board_state_to_str(board)

		elif self.type == GameType.PLAYER_AGAINST_PLAYER:
			pass
		else:
			pass

		if all(map(lambda x : x != '0', self.state)):
			print("Player " + mode(self.state) + " is the winner")



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
	if player1 is None and player2 is None:
		type = GameType.AI_AGAINST_AI
	elif player1 is not None and player2 is None:
		type = GameType.PLAYER_AGAINST_AI
		active_player = player1
	else:
		type = GameType.PLAYER_AGAINST_PLAYER
		active_player = choice([player1, player2])
	new_game = GameBoard(player_1_id = player1, player_2_id = player2, type = type, active_player = active_player)
	db.session.add(new_game)
	db.session.commit()
	return new_game

