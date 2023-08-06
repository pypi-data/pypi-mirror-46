import logging

from packy_agent.exceptions import ImproperlyConfiguredError
from packy_agent.constants import SPEEDTEST_MODULE, SPEEDTEST_MODULE_LOOP
from packy_agent.worker.loops.modules.base import ScheduledProducerTaskLoop, get_target
from packy_agent.domain_logic.models.schematics.speedtest import SpeedtestModuleMeasurement
from packy_agent.domain_logic.modules.speedtest.base import run_speedtest

MBIT = 1000000.0


logger = logging.getLogger(__name__)


def speedtest_impl(*args, **kwargs):
    target = get_target(kwargs, SPEEDTEST_MODULE)
    if not target:
        return

    try:
        target_id = int(target)
    except (ValueError, TypeError):
        raise ImproperlyConfiguredError(f'Speedtest target must be a number (not {target!r})')

    # we place it here because it also saves time momen
    measurement = SpeedtestModuleMeasurement({'target': target})

    results = run_speedtest(target_id)
    measurement.upload_speed = round(results.upload / MBIT, 2)
    measurement.download_speed = round(results.download / MBIT, 2)
    measurement.ping = round(results.ping, 3)

    return measurement


class SpeedtestTaskLoop(ScheduledProducerTaskLoop):

    formal_name = SPEEDTEST_MODULE_LOOP

    def __init__(self, schedule, args=(), kwargs=None, outbound_queue=None):
        super().__init__(schedule=schedule, callable_=speedtest_impl, args=args, kwargs=kwargs,
                         outbound_queue=outbound_queue)
