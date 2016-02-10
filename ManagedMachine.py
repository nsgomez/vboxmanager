import ReferenceMachine
import random
import subprocess
import time

class ManagedMachine:
    def __init__(self, image_name, reference_image, model):
        # type: (str, ReferenceMachine)
        self._image_name = image_name
        self._reference_image = reference_image
        self._is_running = False
        self._is_destroyed = False
        self._model = model


    def _get_image_name(self):
        return self._image_name


    def _get_reference_image(self):
        return self._reference_image 


    def _get_reference_system_name(self):
        return self._reference_image.system_name


    def _get_is_running(self):
        return self._is_running and not self._is_destroyed


    def _get_is_destroyed(self):
        return self._is_destroyed


    def _get_model(self):
        return self._model

    image_name = property(_get_image_name)
    reference_image = property(_get_reference_image)
    system_name = property(_get_reference_system_name)
    is_running = property(_get_is_running)
    is_destroyed = property(_get_is_destroyed)
    model = property(_get_model)


    def start(self):
        # type: bool
        if self._is_running or self._is_destroyed:
            return False

        subprocess.check_output(['VBoxHeadless',
            '--startvm', self._image_name])

        self._is_running = True
        return True


    def stop(self):
        # type: bool
        if not self._is_running or self._is_destroyed:
            return False

        subprocess.check_output(['VBoxManage', 'controlvm',
            self._image_name, 'poweroff'])

        self._is_running = False
        return True


    def restart(self):
        # type: bool
        if not self._is_running or self._is_destroyed:
            return False

        subprocess.check_output(['VBoxManage', 'controlvm',
            self._image_name, 'reset'])

        return True


    def screenshot(self, filename):
        if not self._is_running or self._is_destroyed:
            return False

        if not filename:
            filename = str(time.time())
            suffix = str(random.randint(1, 999))
            filename = filename + suffix

        subprocess.check_output(['VBoxManage', 'controlvm',
            self._image_name, 'screenshot', filename])

        return filename


    def reset_to_reference_state(self):
        # type: ManagedMachine
        self.destroy_machine()

        reference = self._reference_image
        name = self._image_name
        return reference.clone_as_managed_machine(name)


    def destroy(self):
        if self._is_destroyed:
            return

        subprocess.check_output(['VBoxManage',
            'unregistervm', self._image_name, '--delete'])

        self._is_destroyed = True
