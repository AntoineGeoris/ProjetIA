from flask_sqlalchemy import SQLAlchemy
from .views import app
import logging as lg

db = SQLAlchemy(app)

def init_db() :
	db.drop_all()
	db.create_all()
	#requête sql
	db.session.commit()
	lg.warnin('Database initialized !')

#definition des modèles 