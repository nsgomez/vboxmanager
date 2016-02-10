import ManagedMachine
import models
import subprocess

class ReferenceMachine:
    def __init__(self, image_name, system_name, model):
        # type: (str, str)
        self._image_name = image_name
        self._system_name = system_name
        self._model = model


    def _get_image_name(self):
        return self._image_name


    def _get_system_name(self):
        return self._system_name


    def _get_model(self):
        return self._model

    image_name = property(_get_image_name)
    system_name = property(_get_system_name)
    model = property(_get_model)


    """
    Takes the ReferenceMachine and clones it to create a
    ManagedMachine which can be interacted with by the VM
    manager to be wiped or removed at random and infected
    by malware received by email.

    Throws a CalledProcessError exception if VBoxManage
    cannot clone the reference machine properly.
    """
    def clone_as_managed_machine(self, new_image_name):
        # type: (str) -> ManagedMachine        
        subprocess.check_output(['VBoxManage', 'clonevm',
            self._image_name, '--mode', 'machine',
            '--name', new_image_name, '--register'])

        model = models.ManagedMachine()
        model.image_name = new_image_name
        model.reference_image = self._model

        return ManagedMachine(new_image_name, self, model)
