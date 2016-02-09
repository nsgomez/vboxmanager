from peewee import *
import BaseModel

class ReferenceMachine(BaseModel):
    image_name = TextField(unique=True)
    system_name = TextField(unique=True)
