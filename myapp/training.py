from myapp import models, db
import datetime
import logging as lg
import os

NUMBER_OF_SESSIONS = 20             # Number of training session to do (1 training sessiont = 1 commit)
NUMBER_OF_GAME_PER_SESSION = 1000
NUMBER_OF_GAME_FOR_MESSAGE = 100  


games_for_training = lambda nb_games : [models.GameBoard() for _ in range(nb_games)]
epsilon = lambda nb_played_games : max(1 - (nb_played_games / 500000), 0.1)
time_left = lambda time_per_game, nb_games_left : time_per_game * nb_games_left
time_per_game = lambda duration, nb_games_completed : duration / nb_games_completed

def get_games(nb_games):
    games = games_for_training(nb_games)
    for game in games:
        db.session.add(game)
    db.session.commit()
    return games

def init_train():
    os.system('cls')
    models.GameBoard.query.filter_by(no_turn = 0).delete() # Delete unused games from previous trainings
    db.session.commit()
    training_already_completed = models.GameBoard.query.filter_by(type = models.GameType.AI_AGAINST_AI).count()
    eps = epsilon(training_already_completed)
    lg.warning(str(training_already_completed) + " trainings done")

    return eps

def train():
    os.system('cls')
    models.GameBoard.query.filter_by(no_turn = 0).delete() # Delete unused games from previous trainings
    db.session.commit()
    training_already_completed = models.GameBoard.query.filter_by(type = models.GameType.AI_AGAINST_AI).count()
    eps = epsilon(training_already_completed)
    lg.warning(str(training_already_completed) + " already trainings done")
    lg.warning("Training starts")
    start_time = datetime.datetime.now()
    games_completed = 0

    for i in range(NUMBER_OF_SESSIONS):
        games = get_games(NUMBER_OF_GAME_PER_SESSION)
        for game in games:
            while not game.is_gameover():
                game.play(eps = eps)
            games_completed += 1

            if eps > 0.1 and games_completed % 2500 == 0:
                eps -= 0.01

            if games_completed % NUMBER_OF_GAME_FOR_MESSAGE == 0:
                lg.warning("Number of games completed : " + str(games_completed))
                current_time = datetime.datetime.now()
                game_duration = time_per_game(current_time - start_time, games_completed)
                lg.warning("Time left : " + str(time_left(game_duration, (NUMBER_OF_GAME_PER_SESSION * NUMBER_OF_SESSIONS) - games_completed)))

        db.session.commit()
        lg.warning(str(NUMBER_OF_GAME_PER_SESSION) + " games have been committed")
        
    db.session.commit()
    lg.warning("Training is finished")
    lg.warning("Elapsed time : " + str(datetime.datetime.now() - start_time))
    os.system("shutdown /s /t 1") # shutdown computer after training

def train_with_time(hours = 1, minutes = 0, seconds = 0):
    eps = init_train()
    start_time = datetime.datetime.now()
    games_completed = 0
    duration = datetime.timedelta(hours = hours, minutes = minutes, seconds = seconds)
    start_time = datetime.datetime.now()
    current_time = datetime.datetime.now()

    while current_time - start_time <= duration:
        games = get_games(NUMBER_OF_GAME_PER_SESSION)
        games_completed_session = 0
        for game in games:
            while not game.is_gameover():
                game.play(eps = eps)
            games_completed += 1
            games_completed_session += 1

            if eps > 0.1 and games_completed % 2500 == 0:
                eps -= 0.01

            current_time = datetime.datetime.now()

            if games_completed % NUMBER_OF_GAME_FOR_MESSAGE == 0:
                lg.warning("Number of games completed : " + str(games_completed))
                lg.warning("Time left : " + str(duration - (current_time - start_time)))

            if current_time - start_time > duration:
                break;

        db.session.commit()
        lg.warning(str(games_completed_session) + " games have been committed")

    db.session.commit()
    lg.warning("Training is finished. " + str(games_completed) + " games completed")