import ManagedMachine
import ReferenceMachine
import models
import random

class VirusManager:
    def __init__(self, machine_limit = 16):
        self._reference_machines = {}
        self._managed_machines = {}
        self._machine_limit = machine_limit
        self._last_machine_action_time = -1


    def initialize_from_database(self):
        references = models.ReferenceMachine.select()
        for reference in references:
            self.add_machine_from_database(machine)

        machines = models.ManagedMachine.select()
        for machine in machines:
            reference = machine.reference_image.image_name
            reference = self._reference_machines[reference]

            self.add_machine_from_database(machine, reference)

    def add_machine_from_database(self, record, reference):
        name = record.image_name
        machine = ManagedMachine(name, reference, record)

        self._managed_machines[name] = machine


    def add_reference_from_database(self, record):
        image_name = record.image_name
        system_name = record.system_name
        reference = ReferenceMachine(image_name,
            system_name, record)

        self._reference_machines[image_name] = reference


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


    def _get_last_machine_action_time(self):
        return self._last_machine_action_time

    machine_limit = property(_get_machine_limit)
    machine_count = property(_get_machine_count)
    reference_count = property(_get_reference_count)
    managed_machines = property(_get_machines)
    reference_machines = property(_get_references)
    last_machine_action_time = property(
        _get_last_machine_action_time)


    def process(self):
        pass


    def create_new_machine(self, name, reference):
        machine = reference.clone_as_managed_machine(name)
        self._managed_machines[name] = machine


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


    def destroy_machine(self, machine):
        if machine:
            machine.destroy()


    def reset_machine(self, machine):
        if machine:
            machine = machine.reset_to_reference_state()
            name = machine.image_name

            self._managed_machines[name] = machine


    def add_reference_machine(self, reference):
        image_name = reference.image_name
        self._reference_machines[image_name] = reference


    def add_existing_machine(self, machine):
        image_name = machine.image_name
        self._managed_machines[image_name] = machine
