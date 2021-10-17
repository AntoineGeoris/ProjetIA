#required : pip install flask-wtf
#         : pip install email_validator
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

#Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min = 4, max =20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmation mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit_btn  = SubmitField('S\'inscrire')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit_btn  = SubmitField('Se connecter')
