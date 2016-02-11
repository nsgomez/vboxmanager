import Logger
import models
import random
import subprocess
import time

class ReferenceMachine:
    def __init__(self, image_name, system_name):
        # type: (str, str)
        self._image_name = image_name
        self._system_name = system_name


    def _get_image_name(self):
        return self._image_name


    def _get_system_name(self):
        return self._system_name

    image_name = property(_get_image_name)
    system_name = property(_get_system_name)


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
        model.reference_image = self._image_name
        model.save()

        return ManagedMachine(new_image_name, self, model)


class ManagedMachine:
    def __init__(self, image_name, reference_image, model):
        # type: (str, ReferenceMachine)
        self._image_name = image_name
        self._reference_image = reference_image
        self._is_running = False
        self._is_destroyed = False
        self._model = model
        self._logger = Logger.get_logger()
        self._last_screenshot = None


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


    def _get_last_screenshot(self):
        return self._last_screenshot


    def _get_model(self):
        return self._model

    image_name = property(_get_image_name)
    reference_image = property(_get_reference_image)
    system_name = property(_get_reference_system_name)
    is_running = property(_get_is_running)
    is_destroyed = property(_get_is_destroyed)
    last_screenshot = property(_get_last_screenshot)
    model = property(_get_model)


    def stop_silently(self):
        self._logger.info('Attempting to stop ' +
            self._image_name + ' silently')

        subprocess.call(['VBoxManage', 'controlvm',
            self._image_name, 'poweroff'])


    def start(self):
        # type: bool
        if self._is_running or self._is_destroyed:
            return False

        self._logger.info('Starting machine ' + 
            self._image_name)

        self.stop_silently()
        subprocess.check_output(['VBoxManage', 'startvm',
            self._image_name, '--type', 'headless'])

        self._is_running = True
        self._logger.info('Started ' + self._image_name)

        return True


    def stop(self):
        # type: bool
        if not self._is_running or self._is_destroyed:
            return False

        self._logger.info('Stopping machine ' + 
            self._image_name)

        subprocess.check_output(['VBoxManage', 'controlvm',
            self._image_name, 'poweroff'])

        self._is_running = False
        return True


    def restart(self):
        # type: bool
        if not self._is_running or self._is_destroyed:
            return False

        self._logger.info('Restarting machine ' +
            self._image_name)

        subprocess.check_output(['VBoxManage', 'controlvm',
            self._image_name, 'reset'])

        return True


    def screenshot(self, filename):
        if not self._is_running or self._is_destroyed:
            return False

        if not filename:
            prefix = 'store/screenshots/'
            filename = str(time.time())
            suffix = str(random.randint(1, 999))
            filename = prefix + filename + suffix

        self._logger.debug('Screenshotting machine ' +
            self._image_name)

        subprocess.check_output(['VBoxManage', 'controlvm',
            self._image_name, 'screenshot', filename])

        self._last_screenshot = filename
        return filename


    def reset_to_reference_state(self):
        # type: ManagedMachine
        self._logger.info('Resetting machine ' +
            self._image_name + ' to reference state')

        reference = self._reference_image
        name = self._image_name

        self.destroy_machine()
        return reference.clone_as_managed_machine(name)


    def destroy(self):
        if self._is_destroyed:
            return

        self.stop_silently()
        self._logger.info('Destroying machine ' +
            self._image_name)

        subprocess.check_output(['VBoxManage',
            'unregistervm', self._image_name, '--delete'])

        self._model.delete_instance()
        self._is_destroyed = True
