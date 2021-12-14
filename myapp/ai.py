import random
import myapp.models as models
import datetime
import logging as lg

from myapp import db

MOVES = ["down", "up", "left", "right"]

#Description:
	#	This function gives the next move of the AI and update the QTacle
	#Preconditions : 
	# 	- game_board is an instance from the GameBoard class
	#   - board is the state from the game_board in array format 
	# 	- eps >= 0 and eps <= 1
	#Postconditions :
	#	- return the move from the AI
	# 	- QTable score are updated
def get_move(game_board, board, eps):
	qtable_state = game_board.board + game_board.player_1_pos + game_board.player_2_pos + str(game_board.active_player)
	scores = models.QTableState.query.get(qtable_state)

	if scores is None:
		scores = models.QTableState(qtable_state)
		db.session.add(scores)

	if random.uniform(0, 1) < eps:
		move = random.choice(MOVES)
	else:
		max_score_index = [scores.down_score, scores.up_score, scores.left_score, scores.right_score].index(max([scores.down_score, scores.up_score, scores.left_score, scores.right_score]))
		move = MOVES[max_score_index]

	line = int(game_board.player_1_pos[0]) if game_board.active_player == 1 else int(game_board.player_2_pos[0])
	column = int(game_board.player_1_pos[1]) if game_board.active_player == 1 else int(game_board.player_2_pos[1])
	while not game_board.move_allowed(move, game_board.active_player):
		move = random.choice(MOVES)

	if game_board.no_turn >= 2:
		old_board = models.History.query.get((game_board.id, game_board.no_turn - 2)) 
		old_state = old_board.board + old_board.player_1_pos + old_board.player_2_pos + str(game_board.active_player)
		reward = get_reward(game_board.active_player, qtable_state, old_state)
		update_qtable(reward, qtable_state, old_state, old_board.move)

	return move


#Description:
	#	This function calculate the reward gain or lose. (During the game)
	#	One captured cell = 1 point
	# 	The reward is equal to the difference of captured squares between the two players.
	#Preconditions : 
	# 	- state is the actual state from the game
	# 	- old_state is the last state where the active player made a move.
	# 	- active_player is the number of the player who made the move (1 or 2).
	#Postconditions :
	#	- return the reward abtain by the active player negative or positive.
def get_reward(active_player, state, old_state):
    player_1_reward = state[0:25].count("1") - old_state[0:25].count("1")
    player_2_reward = state[0:25].count("2") - old_state[0:25].count("2")

    if active_player == 1:
        return player_1_reward - player_2_reward
    else:
        return player_2_reward - player_1_reward

#Description:
	#	This function update the QTable's score from the corresponding state and action.
	#Preconditions : 
	# 	- reward of the action
	# 	- state of the gameBoard of the initial mov
	#	- state_p1 state of the gameBaord after the move
	# 	- action initial action 
	# 	- action_p1 next_action
	#Postconditions :
	#	- The QTable is update.
def update_qtable(reward, state_p1, state, action):
		score = models.QTableState.query.get(state)
		score_p1 = models.QTableState.query.get(state_p1)

		if score_p1 is None:
			score_p1 = models.QTableState(state_p1)
			db.session.add(score_p1)

		score_p1 = max([score_p1.down_score, score_p1.up_score, score_p1.left_score, score_p1.right_score])

		if action == "left":
			score.left_score = score.left_score + 0.1 * (reward + 0.9 * score_p1 - score.left_score)
		elif action == "right":
			score.right_score = score.right_score + 0.1 * (reward + 0.9 * score_p1  - score.right_score)
		elif action == "up":
			score.up_score = score.up_score + 0.1 * (reward + 0.9 * score_p1 - score.up_score)
		else:
			score.down_score = score.down_score + 0.1 * (reward + 0.9 * score_p1 - score.down_score)

		

#Description:
	#	This function calculate the reward gain or lose. (At the end of the game)
	# 	Winner reward is egal to his own score.
	# 	loser reward is egal to the opposie of the winner's score
	#Preconditions : 
	# 	- game_board is an instnace from the GameBoard class and the the active player must be the winner
	#	- winner_score is the score of the winner's score
	# 	- winner_move is the move of the winner'
	# 	- player_1_is_ia, player_2_is_ia are set to false if player are human
	#Postconditions :
	#	- The QTable is update
def end_game(game_board, winner_score, player_1_is_ia = True):
		winner = game_board.active_player
		loser = 1 if winner == 2 else 2

		winner_state = game_board.board + game_board.player_1_pos + game_board.player_2_pos + str(winner)
		old_winner_board = models.History.query.get((game_board.id, game_board.no_turn - 2))
		old_winner_state = old_winner_board.board + old_winner_board.player_1_pos + old_winner_board.player_2_pos + str(winner)

		loser_board = models.History.query.get((game_board.id, game_board.no_turn - 1))
		loser_state = loser_board.board + loser_board.player_1_pos + loser_board.player_2_pos + str(loser)
		old_loser_board = models.History.query.get((game_board.id, game_board.no_turn - 3))
		old_loser_state = old_loser_board.board + old_loser_board.player_1_pos + old_loser_board.player_2_pos + str(loser)

		if (winner == 1 and player_1_is_ia) or winner == 2:
			update_qtable(winner_score, winner_state, old_winner_state, old_winner_board.move)
		if (loser == 1 and player_1_is_ia) or loser == 2:
			update_qtable(-winner_score, loser_state, old_loser_state, old_loser_board.move)

def train():
	# Games already complete : 30.000
	start_time = datetime.datetime.now()
	eps = 0.99
	num_of_periods = 30
	num_of_games_per_commit = 1000
	for i in range(num_of_periods):
		start_time_period = datetime.datetime.now()
		games = []
		for j in range(num_of_games_per_commit):
			game = models.GameBoard()
			db.session.add(game)
			games.append(game)
		db.session.commit()
		game_completed = 0
		for game in games:
			while not game.is_gameover():
				game.play(eps = 0.99)
			game_completed += 1

			if game_completed % 100 == 0:
				lg.warning(str(game_completed) + " games completed")

		db.session.commit()
		end_time_period = datetime.datetime.now()
		lg.warning(str((i + 1) * num_of_games_per_commit) + " games have been committed")

		if i % 1000 == 0:
			eps -= 0.01
	
	end_time = datetime.datetime.now()

	print("Total time : " + str(end_time - start_time))
	print("Time per game : " + str((end_time - start_time) / (num_of_periods * num_of_games_per_commit)))

	db.session.commit()