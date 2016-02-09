from peewee import *
import BaseModel
import ReferenceMachine

class ManagedMachine(BaseModel):
    image_name = TextField(unique=True)
    reference_image = ForeignKeyField(ReferenceMachine,
        related_name='reference_machine_instances')
