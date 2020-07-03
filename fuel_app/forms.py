from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class registrationForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min = 2, max = 25)])
    email = StringField('E-mail', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6, max = 30)])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), Length(min = 6, max = 30), EqualTo('password')])
    submit = SubmitField('Register')

class loginForm(FlaskForm):
    username = StringField('Username', validators =[DataRequired(), Length(min = 2, max = 25)])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 6, max = 30)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')