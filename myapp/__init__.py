from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'a33653a7074d917291e2b70c227fb065'
db = SQLAlchemy(app)

from myapp import views
from myapp import models
models.db.init_app(app)

@app.cli.command("init_db")
def init_db() :
	models.init_db()

