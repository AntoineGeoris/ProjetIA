from flask_sqlalchemy import SQLAlchemy
from .views import app
import logging as lg

db = SQLAlchemy(app)

def init_db() :
	db.drop_all()
	db.create_all()
	db.session.commit()
	lg.warning('Database initialized !') 