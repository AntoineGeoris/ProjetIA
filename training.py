from myapp import models, db
import datetime
import logging as lg
import os

NUMBER_OF_SESSIONS = 100             # Number of training session to do (1 training sessiont = 1 commit)
NUMBER_OF_GAME_PER_SESSION = 1000    


games_for_training = lambda nb_games : [models.GameBoard() for _ in range(nb_games)]
epsilon = lambda nb_played_games : max(nb_played_games / 100000, 0.1)
time_left = lambda time_per_game, nb_games_left : time_per_game * nb_games_left
time_per_game = lambda duration, nb_games_completed : duration / nb_games_completed

def get_games(nb_games):
    games = games_for_training(nb_games)
    for game in games:
        db.session.add(game)
    db.session.commit()
    return games

def train():
    os.system('cls')
    models.GameBoard.query.filter_by(no_turn = 0).delete() # Delete unused games from previous trainings
    db.session.commit()
    eps = epsilon(models.GameBoard.query.filter_by(type = models.GameType.AI_AGAINST_AI).count())
    lg.warning("Training starts")
    start_time = datetime.datetime.now()
    games_completed = 0

    for i in range(NUMBER_OF_SESSIONS):
        games = get_games(NUMBER_OF_GAME_PER_SESSION)
        for game in games:
            while not game.is_gameover():
                game.play(eps = eps)
            games_completed += 1

            if games_completed % 1000 == 0:
                eps -= 0.01

        db.session.commit()
        end_time = datetime.datetime.now()
        game_duration = time_per_game(end_time - start_time, games_completed)
        lg.warning(str(NUMBER_OF_GAME_PER_SESSION) + " games have been committed")
        lg.warning("Number of games completed : " + str(games_completed))
        lg.warning("Time left : " + str(time_left(game_duration, (NUMBER_OF_GAME_PER_SESSION * NUMBER_OF_SESSIONS) - games_completed)))

    db.session.commit()
    lg.warning("Training is finished")
    """os.system("shutdown /s /t 1")""" # shutdown computer after training