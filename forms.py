from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtfpeewee.orm import model_form
from models import *    


class NewsForm(FlaskForm):
    url = StringField('Link', validators=[
        DataRequired(), Length(min = 5, max=100)
    ])

SimpleNewsForm = model_form(News)

"""class SubscriptionForm(FlaskForm):
    bdnews = News()
    news = bdnews.get(url = HiddenField("Feed"))

SimpleSubscriptionForm = model_form(News)"""

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(min = 5, max=30)
    ])
    password = StringField('Password', validators=[
        DataRequired(), Length(min = 5, max=30)
    ])

SimpleLoginForm = model_form(Users)

class SignupForm(FlaskForm):
    firstname = StringField('Firstname', validators=[
        DataRequired(), Length(min = 5, max=30)
    ])
    lastname = StringField('Lastname', validators=[
        DataRequired(), Length(min = 5, max=30)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Length(min = 5, max=30)
    ])
    password = StringField('Password', validators=[
        DataRequired(), Length(min = 5, max=30)
    ])

SimpleSignupForm = model_form(Users)