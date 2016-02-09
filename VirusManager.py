import ManagedMachine
import ReferenceMachine
import models

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

        self._reference_machines[name] = reference


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
        pass


    def wipe_random_machine(self):
        pass


    def wipe_machine(self, machine):
        pass


    def add_reference_machine(self, reference):
        pass


    def add_existing_machine(self, machine):
        pass
