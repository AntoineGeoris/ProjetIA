from myapp import models, ai, db

def train():
    for i in range(100):
        game = models.GameBoard()

        game