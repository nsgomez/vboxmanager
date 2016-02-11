from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('store/virus_manager.db')
class BaseModel(Model):
    class Meta:
        database = db

class ManagedMachine(BaseModel):
    image_name = TextField(unique=True)
    reference_image = TextField()

db.create_tables([ManagedMachine], True)