import time
import logging

from requests.exceptions import ConnectionError

from packy_agent.constants import (
    PING_MODULE, TRACE_MODULE, SPEEDTEST_MODULE, HTTP_MODULE, SUBMITTER_LOOP, ErrorSide)
from packy_agent.worker.loops.base.periodic import PeriodicLoop
from packy_agent.clients.local_storage import get_local_storage, TYPE_MAP
from packy_agent.configuration.settings import settings
from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.exceptions import CoolDown


MEASUREMENTS_LIMIT = 100
MODULE_PUBLIC_IDENTIFIER_MAP = {
    1: PING_MODULE,
    2: TRACE_MODULE,
    3: SPEEDTEST_MODULE,
    4: HTTP_MODULE,
}
assert len(MODULE_PUBLIC_IDENTIFIER_MAP) == len(TYPE_MAP)

logger = logging.getLogger(__name__)


def is_invalid_chronological_order(response):
    if not response.status_code == 400:
        return False

    response_json = response.json()
    if not isinstance(response_json, dict):
        return False

    errors = response_json.get('errors')
    if not isinstance(errors, dict):
        return False

    non_field_errors = errors.get('non_field_errors')
    if not non_field_errors or not isinstance(non_field_errors, list):
        return False

    for item in non_field_errors:
        if item.get('code') == 'invalid-chronological-order':
            return True

    return False


def submit_measurement(measurement_row):
    module_public_identifier = MODULE_PUBLIC_IDENTIFIER_MAP.get(measurement_row.measurement_type)
    if not module_public_identifier:
        logger.warning('Unknown measurement type: %s', measurement_row.measurement_type)
        return

    local_storage = get_local_storage()
    value = measurement_row.value
    try:
        response = get_packy_server_client().submit_measurement(
            module_public_identifier, value, raise_for_status=False)
    except ConnectionError as ex:
        logger.info(f'Could not connect to server to submit measurement of '
                    f'{module_public_identifier} ({ex!r}): {value}')
        local_storage.save_measurement_error(
            measurement_row.id, ErrorSide.SERVER.value, f'Could not connect to server: {ex!r}')
        raise CoolDown()
    except Exception as ex:
        logger.exception(
            f'Error while submitting measurement of {module_public_identifier}: {value}')
        local_storage.save_measurement_error(
            measurement_row.id, ErrorSide.CLIENT.value, repr(ex) or 'Unknown')
        raise CoolDown()

    status_code = response.status_code
    if 200 <= status_code < 300:
        local_storage.mark_measurement_as_submitted(measurement_row.id)
        return
    else:
        if status_code >= 500:
            error_side = ErrorSide.SERVER.value
            log_method = logger.warning  # because it is server error
            cool_down = True
        else:
            error_side = ErrorSide.CLIENT.value
            if is_invalid_chronological_order(response):
                # Marking as submitted is actually a kind of hack
                local_storage.mark_measurement_as_submitted(measurement_row.id)
                log_method = logger.warning
                cool_down = False
            else:
                log_method = logger.error  # because it is our error
                cool_down = True

        log_method(f'Server responded with HTTP{status_code}: {response.content}')
        local_storage.save_measurement_error(
            measurement_row.id, error_side, f'HTTP{status_code}: {response.content}')

        if cool_down:
            raise CoolDown()


class TaskResultsSubmitter(PeriodicLoop):

    formal_name = SUBMITTER_LOOP

    def __init__(self):
        self.results_submission_period_seconds = settings.get_worker_results_submission_period_seconds()

        super().__init__(self.results_submission_period_seconds)
        self.submitted_counter = 0

    def call(self):
        start_time = time.time()
        max_submit_time = 0
        least_period_seconds = self.results_submission_period_seconds * (1 - self.jitter_factor)

        local_storage = get_local_storage()
        results_submission_pause_seconds = settings.get_worker_results_submission_pause_seconds()
        for measurement_type, module_name in MODULE_PUBLIC_IDENTIFIER_MAP.items():
            logger.debug('Submitting measurements for %s module...', module_name)

            measurements = local_storage.get_remaining_measurements(
                measurement_type, limit=MEASUREMENTS_LIMIT)

            measurements_count = len(measurements)
            if measurements_count >= MEASUREMENTS_LIMIT:
                logger.warning('Retrieved %s measurements', measurements_count)

            for measurement_row in measurements:
                try:
                    start_submit_time = time.time()
                    submit_measurement(measurement_row)
                    max_submit_time = max(max_submit_time, time.time() - start_submit_time)
                    self.submitted_counter += 1
                except CoolDown:
                    break
                finally:
                    if least_period_seconds - (time.time() - start_time) < max_submit_time * 1.5:
                        return

                    self.sleep(results_submission_pause_seconds)
                    if self.is_stopping or not self.is_running:
                        return
