import ConfigManager
import Logger
from ManagedMachine import ManagedMachine
from ReferenceMachine import ReferenceMachine

import models
import random
import time

class VirusManager:
    def __init__(self, machine_limit = 8):
        now = time.time()

        self._reference_machines = {}
        self._managed_machines = {}
        self._machine_limit = machine_limit
        self._last_create_time = now
        self._last_destroy_time = now
        self._last_reset_time = now
        self._last_screenshot_time = now
        self._logger = Logger.get_logger()
        self.initialize()


    def initialize(self):
        config = ConfigManager.get_data()
        for reference in config['references']:
            self.add_reference_from_yaml(reference)

        machines = models.ManagedMachine.select()
        for machine in machines:
            reference = machine.reference_image.image_name
            reference = self._reference_machines[reference]

            self.add_machine_from_database(machine, reference)

            name = machine.image_name
            machine = self._managed_machines[name]
            machine.start()

    def add_machine_from_database(self, record, reference):
        name = record.image_name
        machine = ManagedMachine(name, reference, record)

        self._managed_machines[name] = machine
        self._logger.info('Imported machine ' + name)


    def add_reference_from_yaml(self, record):
        image_name = record['image_name']
        system_name = record['system_name']
        reference = ReferenceMachine(image_name,
            system_name)

        self._reference_machines[image_name] = reference
        self._logger.info('Imported reference ' +
            image_name)

    def _get_machine_limit(self):
        return self._machine_limit


    def _get_machine_count(self):
        return len(self._managed_machines)


    def _get_reference_count(self):
        return len(self._reference_machines)


    def _get_references(self):
        return self._reference_machines


    def _get_machines(self):
        return self._managed_machines


    def _get_last_destroy_time(self):
        return self._last_destroy_time


    def _get_last_create_time(self):
        return self._last_create_time


    def _get_last_reset_time(self):
        return self._last_reset_time


    def _get_last_screenshot_time(self):
        return self._last_screenshot_time

    machine_limit = property(_get_machine_limit)
    machine_count = property(_get_machine_count)
    reference_count = property(_get_reference_count)
    managed_machines = property(_get_machines)
    reference_machines = property(_get_references)
    last_destroy_time = property(_get_last_destroy_time)
    last_create_time = property(_get_last_create_time)
    last_reset_time = property(_get_last_reset_time)
    last_screenshot_time = property(
        _get_last_screenshot_time)
    

    def gen_image_name(self, index):
        return "Sandbox Image " + str(index)


    def get_free_index(self):
        if self.machine_count >= self.machine_limit:
            return None

        i = 1
        while i <= self.machine_limit:
            key = self.gen_image_name(i)
            if key not in self._managed_machines:
                return i

            i = i + 1

        return None


    def create_new_machine(self, name, reference):
        self._logger.info('Creating new machine ' + name +
            'from reference ' + reference.image_name)

        machine = reference.clone_as_managed_machine(name)
        self._managed_machines[name] = machine
        self._last_create_time = time.time()


    def destroy_random_machine(self):
        machine = self.get_random_machine()
        if machine:
            self.destroy_machine(machine)


    def reset_random_machine(self):
        machine = self.get_random_machine()
        if machine:
            machine = self.reset_machine(machine)


    def get_random_machine(self):
        if self.machine_count < 1:
            return None

        keys = list(self._managed_machines.keys())
        key = random.choice(keys)
        machine = self._managed_machines[key]

        return machine


    def get_random_reference(self):
        if self.reference_count < 1:
            return None

        keys = list(self._reference_machines.keys())
        key = random.choice(keys)
        reference = self._reference_machines[key]

        return reference


    def destroy_machine(self, machine):
        if machine:
            name = machine.image_name
            machine.destroy()

            self._managed_machines.pop(name, None)
            self._last_destroy_time = time.time()


    def reset_machine(self, machine):
        if machine:
            machine = machine.reset_to_reference_state()
            name = machine.image_name

            self._managed_machines[name] = machine
            self._last_reset_time = time.time()


    def add_reference_machine(self, reference):
        image_name = reference.image_name
        self._reference_machines[image_name] = reference
        self._logger.info('Added reference ' + image_name)


    def add_existing_machine(self, machine):
        image_name = machine.image_name
        self._managed_machines[image_name] = machine
        self._logger.info('Added machine ' + image_name)
