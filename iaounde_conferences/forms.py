from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, URLField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional, Email, EqualTo, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class ConferenceForm(FlaskForm):
    nom = StringField('Nom de la conférence', validators=[
        DataRequired(message='Le nom est requis'),
        Length(min=3, max=200)
    ])
    periode_debut = DateField('Date de début', validators=[DataRequired()])
    periode_fin = DateField('Date de fin', validators=[DataRequired()])
    logo = FileField('Logo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    lien_site = URLField('Lien du site', validators=[DataRequired(), URL()])
    submit = SubmitField('Enregistrer')

class UserForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), EqualTo('password')
    ])
    role = SelectField('Rôle', choices=[('admin', 'Administrateur'), ('super_admin', 'Super Admin')], default='admin')
    is_active = BooleanField('Actif', default=True)
    submit = SubmitField('Créer')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur existe déjà.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email existe déjà.')