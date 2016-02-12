from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('store/virus_manager.db',
    threadlocals=True)

class BaseModel(Model):
    class Meta:
        database = db


class ManagedMachine(BaseModel):
    image_name = TextField(unique=True)
    reference_image = TextField()
    creation_time = IntegerField()


class Infection(BaseModel):
    name = TextField()
    machine = ForeignKeyField(ManagedMachine,
        related_name='infections')

db.create_tables([ManagedMachine, Infection], True)
