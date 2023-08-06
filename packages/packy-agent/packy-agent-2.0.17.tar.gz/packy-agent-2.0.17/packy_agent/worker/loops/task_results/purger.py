import logging
import os.path

from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.clients.local_storage import get_local_storage
from packy_agent.configuration.settings import settings
from packy_agent.utils.fs import get_available_disk_space
from packy_agent.constants import PURGER_LOOP

MIN_SPACE_TO_FREE = 8192


logger = logging.getLogger(__name__)


def purge():
    local_storage = get_local_storage()
    deleted_counter = local_storage.purge_submitted_measurements()
    deleted_counter += local_storage.purge_failed_measurements()

    logger.debug('Evaluating a need to purge unsubmitted measurements...')

    minimum_disk_space_bytes = settings.get_minimum_disk_space_bytes()
    available_disk_space = get_available_disk_space()
    if available_disk_space < minimum_disk_space_bytes:
        logger.debug('Need to purge unsubmitted measurements')
        to_free = minimum_disk_space_bytes - available_disk_space
        if to_free >= MIN_SPACE_TO_FREE:
            number_of_records = local_storage.get_measurements_number()
            logger.debug('Found %s unsubmitted measurements', number_of_records)
            if number_of_records:
                file_size = os.path.getsize(settings.get_database_filename())
                bytes_per_record = file_size / number_of_records
                records_to_delete = int(to_free / bytes_per_record)
                logger.debug('Will purge %s unsubmitted measurements', records_to_delete)
                deleted_counter += local_storage.purge_unsubmitted_measurements(
                    records_to_delete)

    return deleted_counter


class TaskResultsPurger(PeriodicLoop):

    formal_name = PURGER_LOOP

    def __init__(self):
        super().__init__(settings.get_worker_purge_period_seconds())
        self.purged_records = 0

    def call(self):
        purged_records = purge()
        self.purged_records += purged_records

