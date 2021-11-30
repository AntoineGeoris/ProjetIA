import random
import myapp.models as models

from myapp import db

class AI:

	def get_move(self, game_board, board, eps):
		state = game_board.board + game_board.player_1_pos + game_board.player_2_pos + str(game_board.active_player)
		move = self.get_action(state, eps)

		line = int(game_board.player_1_pos[0]) if game_board.active_player == 1 else int(game_board.player_2_pos[0])
		column = int(game_board.player_1_pos[1]) if game_board.active_player == 1 else int(game_board.player_2_pos[1])
		while not game_board.move_allowed(move, line, column, board, game_board.active_player):
			move = self.get_action(state, eps)

		if game_board.no_turn >= 2:
			old_board = models.History.query.get((game_board.id, game_board.no_turn - 2)) 
			old_state = old_board.board + old_board.player_1_pos + old_board.player_2_pos + str(game_board.active_player)
			reward = self.reward(game_board.active_player, state, old_state)
			self.updateQTable(reward, state, old_state, old_board.move, move)

		return move;

	def get_action(self, state, eps):
		score = models.QTableState.query.get(state)
		score_is_none = score is None

		if score_is_none:
			score = models.QTableState(state = state)
			db.session.add(score)
			db.session.commit()

		if random.uniform(0, 1) < eps or score_is_none: 
			action = random.choice(['left', 'right', 'up', 'down'])
		else:
			index = [score.down_score, score.up_score, score.left_score, score.right_score].index(max([score.down_score, score.up_score, score.left_score, score.right_score]))

			if index == 0:
				action = "down"
			elif index == 1:
				action = "up"
			elif index == 2:
				action = "left"
			else:
				action = "right"

		return action

	def reward(self, active_player, state, old_state):
		player_1_reward = state[0:25].count("1") - old_state[0:25].count("1")
		player_2_reward = state[0:25].count("2") - old_state[0:25].count("2")

		if active_player == 1:
			return player_2_reward - player_1_reward
		else:
			return player_1_reward - player_2_reward

	def updateQTable(self, reward, state, old_state, action, action_p1):
		score = models.QTableState.query.get(old_state)
		score_p1 = models.QTableState.query.get(state)

		if action_p1 == "left":
			score_p1 = score_p1.left_score
		elif action_p1 == "right":
			score_p1 = score_p1.right_score
		elif action_p1 == "up":
			score_p1 = score_p1.up_score
		else:
			score_p1 = score_p1.down_score

		if action == "left":
			score.left_score = score.left_score + 0.1 * (reward + 0.9 * score_p1 - score.left_score)
		elif action == "right":
			score.right_score = score.right_score + 0.1 * (reward + 0.9 * score_p1  - score.right_score)
		elif action == "up":
			score.up_score = score.up_score + 0.1 * (reward + 0.9 * score_p1 - score.up_score)
		else:
			score.down_score = score.down_score + 0.1 * (reward + 0.9 * score_p1 - score.down_score)

		db.session.commit()