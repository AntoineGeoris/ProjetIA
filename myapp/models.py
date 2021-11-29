#from sqlalchemy.orm import backref
from myapp import db, login_manager
from myapp.ia import AI
from datetime import datetime
from enum import IntEnum
import logging as lg
from random import choice
from flask_login import UserMixin

def init_db() :
	db.drop_all()
	db.create_all()
	db.session.commit()
	lg.warning('Database initialized !') 

@login_manager.user_loader				# décorator, it just need to be that way, check documentation for more info
def load_player(player_id):
	return Player.query.get(int(player_id)) 


class GameType(IntEnum):
	AI_AGAINST_AI = 1
	PLAYER_AGAINST_AI = 2
	PLAYER_AGAINST_PLAYER = 3

	#Will probably have changes in the DB implementation, testing purpose

class GameBoard(db.Model):
	BOARD_SIZE = 5

	id = db.Column(db.Integer, primary_key = True)
	player_1_pos = db.Column(db.String(2), nullable = False)
	player_2_pos = db.Column(db.String(2), nullable = False)
	date_played = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	no_turn = db.Column(db.Integer, nullable = False, default = "0")
	board = db.Column(db.String(25), nullable = False)
	type = db.Column(db.Integer, nullable = False, default = GameType.PLAYER_AGAINST_AI)
	active_player = db.Column(db.Integer, nullable = True)
	player_1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)
	player_2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable = True)

	def __init__(self, **kwargs):
		super(GameBoard, self).__init__(**kwargs)
		self.board = "1"
		for i in range((self.BOARD_SIZE ** 2) - 2):
			self.board += "0"
		self.board += "2"
		self.player_1_pos = "00"
		self.player_2_pos = str(self.BOARD_SIZE - 1) * 2


	def __game_board_state_to_str(self, board):
		string = ""
		for i in range(self.BOARD_SIZE):
			string += "".join(board[i])
		self.board = string

	def game_board_state_from_str(self):
		board = []
		for i in range(1,self.BOARD_SIZE + 1):
			line = []
			for y in range((i - 1) * self.BOARD_SIZE, i * self.BOARD_SIZE):
				line.append(self.board[y])
			board.append(line)
		return board

	def score(self, player_number):
		board = self.game_board_state_from_str()

		score = lambda player_number, board : 0 if len(board) <= 0 else board[0].count(player_number) + score(player_number, board[1:])

		return score(player_number, board)

	def is_gameover(self):
		return all(map(lambda x : x != '0', self.board))

	def move_allowed(self, move, line, column, board, num_player):
		if move == "right":
			return column + 1 < self.BOARD_SIZE and (board[line][column + 1] == '0' or board[line][column + 1] == str(num_player))
		if move == "left":
			return column - 1 >= 0 and (board[line][column - 1] == '0' or board[line][column - 1] == str(num_player))
		if move == "up":
			return line - 1 >= 0 and (board[line - 1][column] == '0' or board[line - 1][column] == str(num_player))
		
		return line + 1 < self.BOARD_SIZE and (board[line + 1][column] == '0' or board[line + 1][column] == str(num_player))

	def move(self, move, num_player, board, line, column):		
		if move == "right":
			column += 1
		elif move == "left":
			column -= 1
		elif move == "up":
			line -= 1
		else:
			line += 1
		
		board[line][column] = str(num_player)
		flags = self.enclosure(board, num_player)

		for i in range(self.BOARD_SIZE):
			for j in range(self.BOARD_SIZE):
				if flags[i][j]:
					board[i][j] = str(num_player)

		if num_player == 1:
			self.player_1_pos = str(line) + str(column)
		else:
			self.player_2_pos = str(line) + str(column)

		return board
			
	def enclosure(self, board, num_player):
		freeCells = 0
		flags = [[True] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
		for line in range(len(flags)):
			for column in range(len(flags[line])):
				flags[line][column] = board[line][column] in ('0', str(num_player))
				freeCells += 1 if board[line][column] == '0' else 0

		for i in range(freeCells):
			for line in range(len(flags)):
				for column in range(len(flags[line])):
					if not flags[line][column]:
						if line - 1 >= 0 and board[line - 1][column] == '0':
							flags[line - 1][column] = False
						if line + 1 < self.BOARD_SIZE and board[line + 1][column] == '0':
							flags[line + 1][column] = False
						if column - 1 >= 0 and board[line][column - 1] == '0':
							flags[line][column - 1] = False
						if column + 1 < self.BOARD_SIZE and board[line][column + 1] == '0':
							flags[line][column + 1] = False

		return flags

	def save_state(self, move):
		old_state = History(no_turn = self.no_turn, move = move, board = self.board, player_1_pos = self.player_1_pos, player_2_pos = self.player_2_pos, game_board_id = self.id)
		db.session.add(old_state)
		db.session.commit()		
					
	def play(self, move):
		ia = AI()
		board = self.game_board_state_from_str()
		if self.type == GameType.PLAYER_AGAINST_AI:
			line = int(self.player_1_pos[0])
			column = int(self.player_1_pos[1])

			if self.move_allowed(move, line, column, board, 1):
				board = self.move(move, 1, board, line, column)
				self.no_turn += 1;
				self.__game_board_state_to_str(board)
				self.save_state(move)

				move = ia.get_move(self.id, self.board, self.player_1_pos, self.player_2_pos, self.no_turn, 2)
				line = int(self.player_2_pos[0])
				column = int(self.player_2_pos[1])
				while not self.move_allowed(move, line, column, board, 2):
					move = ia.get_move(self.id, self.board, self.player_1_pos, self.player_2_pos, self.no_turn, 2)
				
				board = self.move(move, 2, board, line, column)

				self.no_turn += 1
				self.__game_board_state_to_str(board)
				self.save_state(move)

		elif self.type == GameType.PLAYER_AGAINST_PLAYER:
			pass
		else:
			pass

class Player(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique = True, nullable = False)
	username = db.Column(db.String(30), unique = True, nullable = False)
	password = db.Column(db.String(20), nullable = False)
	image_file = db.Column(db.String(30), nullable = True, default = "default.jpg")

	def __repr__(self):
		return f"User : ({self.id}) {self.username}"

class History(db.Model) :
	game_board_id = db.Column(db.Integer, db.ForeignKey('game_board.id'), primary_key = True) # ????
	no_turn = db.Column(db.Integer, primary_key = True)
	player_1_pos = db.Column(db.String(2), nullable = False)
	player_2_pos = db.Column(db.String(2), nullable = False)
	board = db.Column(db.String(25), nullable = False)
	move =  db.Column(db.String(5))
	

class QTableState(db.Model):
	state = db.Column(db.String(32), primary_key = True) #25 board + 3 digits turn no + 4 digits for player position ? Primary key ? 
	left_score = db.Column(db.Integer, default=0)
	right_score = db.Column(db.Integer, default=0)
	up_score = db.Column(db.Integer, default=0)
	down_score = db.Column(db.Integer, default=0)

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