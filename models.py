from peewee import SqliteDatabase
from peewee import Model
from peewee import TextField
from peewee import DateTimeField
from peewee import ForeignKeyField
from datetime import datetime
from wtfpeewee.orm import model_form


database = SqliteDatabase('lecteur_flux.sqlite3')

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    firstname = TextField()
    lastname = TextField()
    email = TextField(unique=True)
    password = TextField()
    created_at = DateTimeField(default=datetime.now)

class News(BaseModel):
    url = TextField(unique=True)
    user = ForeignKeyField(Users, backref = "lecteur_flux")
    created_at = DateTimeField(default=datetime.now)

class Subscription(BaseModel):
    user = ForeignKeyField(Users, backref = "lecteur_flux")
    news = ForeignKeyField(News, backref = "lecteur_flux")


def create_tables():
    with database:
        database.create_tables([ Users, News, Subscription])


def drop_tables():
    with database:
        database.drop_tables([Users, News, Subscription])

SimpleNewsForm = model_form(News)