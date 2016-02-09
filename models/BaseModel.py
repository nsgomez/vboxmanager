from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('virus_manager.db')

class BaseModel(Model):
    class Meta:
        database = db
