from VirusManager import VirusManager
import ConfigManager
import Logger
import json
import random
import requests
import time

# Destroy a random machine at least once every four hours.
DESTROY_DELAY = (60 * 60 * 4)
RESET_DELAY = DESTROY_DELAY

# Create a machine at random at least once every three
# hours.
CREATE_DELAY = (60 * 60 * 3)

# Take screenshots every 30sec.
SCREENSHOT_DELAY = 30

def main():
    manager = VirusManager()
    logger = Logger.get_logger()

    process_updates(manager, logger)
    logger.info('VirusManager now ready for processing')

    while True:
        try:
            process(manager, logger)
            time.sleep(1)
        except KeyboardInterrupt:
            break

def process(manager, logger):
    updates_pending = False

    #logger.debug('Processing a manager tick')
    if manager.machine_count > manager.machine_limit:
        manager.destroy_random_machine()
        updates_pending = True

    now = time.time()
    time_delta = now - manager.last_destroy_time

    # If it's been long enough since a machine was
    # destroyed, we have a 0.1% chance of destroying
    # one now.
    if  time_delta > DESTROY_DELAY \
    and random.random() <= 0.001:
        logger.info('Destroying a machine at random...')
        manager.destroy_random_machine()
        updates_pending = True

    time_delta = now - manager.last_reset_time

    # Likewise, we have a 0.05% chance of resetting a
    # random machine now.
    if  time_delta > RESET_DELAY \
    and random.random() <= 0.0005:
        logger.info('Resetting a machine at random...')
        manager.reset_random_machine()
        updates_pending = True

    time_delta = now - manager.last_create_time

    # Likewise, we have a 0.1% chance of creating a
    # new machine now.
    if time_delta > CREATE_DELAY \
    and random.random() <= 0.001:
        reference = manager.get_random_reference()
        index = manager.get_free_index()
        name = manager.gen_image_name(index)

        logger.info('Creating a random machine...')
        machine = manager.create_new_machine(name,
            reference)

        machine.start()
        updates_pending = True

    time_delta = now - manager.last_screenshot_time
    if time_delta > SCREENSHOT_DELAY:
        logger.info('Screenshotting all machines...')
        manager.screenshot_all_machines()
        updates_pending = True

    if updates_pending:
        process_updates(manager, logger)

def process_updates(manager, logger):
    payload = []
    for key in manager.managed_machines:
        machine = manager.managed_machines[key]

        image_name = machine.image_name
        system_name = machine.system_name
        screenshot_filename = machine.last_screenshot
        infections = []

        machine = {}
        machine['image_name'] = image_name
        machine['system_name'] = system_name
        machine['screenshot_filename'] = screenshot_filename
        machine['infections'] = infections

        payload.append(machine)

    payload = json.dumps(payload)
    requests.post('http://127.0.0.1:5000/update', payload)

if __name__ == '__main__':
    main()
