import ConfigManager
import Logger
import random
import time
from VirusManager import VirusManager

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

    while True:
        try:
            process(manager, logger)
            time.sleep(1)
        except KeyboardInterrupt:
            break

def process(manager, logger):
    if manager.machine_count > manager.machine_limit:
        manager.destroy_random_machine()

    now = time.time()
    time_delta = now - manager.last_destroy_time

    # If it's been long enough since a machine was
    # destroyed, we have a 0.01% chance of destroying
    # one now.
    if  time_delta > DESTROY_DELAY \
    and random.random() <= 0.0001:
        logger.info('Destroying a machine at random...')
        manager.destroy_random_machine()

    time_delta = now - manager.last_reset_time

    # Likewise, we have a 0.05% chance of resetting a
    # random machine now.
    if  time_delta > RESET_DELAY \
    and random.random() <= 0.0005:
        logger.info('Resetting a machine at random...')
        manager.reset_random_machine()

    time_delta = now - manager.last_create_time

    # Likewise, we have a 0.05% chance of creating a
    # new machine now.
    if time_delta > CREATE_DELAY \
    and random.random() <= 0.0005:
        reference = manager.get_random_reference()
        index = manager.get_free_index()
        name = manager.gen_image_name(index)

        logger.info('Creating a random machine...')
        machine = manager.create_new_machine(name,
            reference)

        machine.start()

    time_delta = now - self._last_screenshot_time
    if time_delta > SCREENSHOT_DELAY:
        pass

if __name__ == '__main__':
    main()
