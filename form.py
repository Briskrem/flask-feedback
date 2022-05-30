from xxlimited import Str
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, length

class AddUser(FlaskForm):
    username =StringField('username', validators=[InputRequired(), length(max=30)])
    password =PasswordField('password', validators=[InputRequired()])
    email =EmailField('email', validators=[InputRequired(), length(max=50)])
    first_name =StringField('first_name', validators=[InputRequired(), length(max=30)])
    last_name =StringField('last_name', validators=[InputRequired(), length(max=30)])


class LoginForm(FlaskForm):
    username =StringField('username', validators=[InputRequired(), length(max=30)])
    password =PasswordField('password', validators=[InputRequired()])


class AddFeedback(FlaskForm):
    title = StringField('title', validators=[InputRequired(), length(max=30)])
    content = StringField('content', validators=[InputRequired(), length(max=500)])