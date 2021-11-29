import random
import myapp.models as models
from myapp import db

class AI:

	def get_move(self, game_board_id, board, player_1_pos, player_2_pos, turn_no, active_player):
		state = board + player_1_pos + player_2_pos + str(turn_no)
		move = self.get_action(state, 0.4)

		if turn_no >= 2:
			old_board = models.History.query.get((game_board_id, turn_no - 2)) 
			old_state = old_board.board + old_board.player_1_pos + old_board.player_2_pos + str(turn_no - 2)
			reward = self.reward(active_player, state, old_state)
			self.updateQTable(reward, state, old_state, old_board.move, move)

		return move;

	def get_action(self, state, eps):
		score = models.QTableState.query.get(state)

		if score is None:
			score = models.QTableState(state = state)
			db.session.add(score)
			db.session.commit()

		if random.uniform(0, 1) < eps:
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