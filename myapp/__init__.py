import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'a33653a7074d917291e2b70c227fb065'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'  #use bootstrap classes to display message asking for login when accessing restricted page
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'proj.ai.maki@gmail.com' #Would be better to use environment variables, but this will be enough for this project ?
app.config['MAIL_PASSWORD'] = 'Tigrou007' #see above
mail = Mail(app)

from myapp import views
from myapp import models
from myapp import training
models.db.init_app(app)

@app.cli.command("init_db")
def init_db() :
	models.init_db()

@app.cli.command("train")
def train():
	training.train()

@app.cli.command("train_with_time")
@click.option("--hours", default = 1)
@click.option("--minutes", default = 0)
@click.option("--seconds", default = 0)
def train_with_time(hours, minutes, seconds):
	training.train_with_time(hours=hours, minutes = minutes, seconds=seconds)

