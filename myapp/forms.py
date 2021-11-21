from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, ValidationError
from myapp.models import Player

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min = 4, max =20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password_confirm = PasswordField('Confirmation mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit_btn  = SubmitField('S\'inscrire')

    def validate_username(self, username):
        player = Player.query.filter_by(username=username.data).first()
        if player:
            raise ValidationError('Oh non, ce pseudo est déjà utilisé :(')
    
    def validate_email(self, email):
        player = Player.query.filter_by(email=email.data).first()
        if player:
            raise ValidationError('Un compte existant utilise déjà cette adresse e-mail\n')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit_btn  = SubmitField('Se connecter')

class UpdateAccountForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min = 4, max =20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Photo de profil', validators=[FileAllowed(['jpg','png'])])
    submit_btn  = SubmitField('Mettre à jour')

    def validate_username(self, username):
        if username.data != current_user.username :
            player = Player.query.filter_by(username=username.data).first()
            if player:
                raise ValidationError('Oh non, ce pseudo est déjà utilisé :(')
    
    def validate_email(self, email):
        if email.data != current_user.email :
            player = Player.query.filter_by(email=email.data).first()
            if player:
                raise ValidationError('Un compte existant utilise déjà cette adresse e-mail\n')