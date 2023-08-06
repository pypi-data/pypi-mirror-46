import logging

from packy_agent.constants import HTTP_MODULE_LOOP
from packy_agent.worker.loops.modules.base import ScheduledProducerTaskLoop
from packy_agent.domain_logic.modules.http.base import get_http_measurement

MBIT = 1000000.0


logger = logging.getLogger(__name__)


def http_impl(*args, **kwargs):
    url = kwargs.get('url')
    if not url:
        logger.debug('URLs are not configured for `http` module')
        return

    follow_redirects = kwargs.get('follow_redirects', False)

    # TODO(dmu) MEDIUM: Figure out what happens inside `curl` library and remove this
    #                   workaround
    for _ in range(10):
        measurement = get_http_measurement(url, follow_redirects=follow_redirects)
        if not measurement.is_success or (measurement.total_ms < 4000000 and
                                          measurement.namelookup_ms < 4000000):
            break  # we got the measurement
    else:
        measurement = None
        logger.error('Failed to get proper measurement from curl for %s', url)

    return measurement


class HTTPTaskLoop(ScheduledProducerTaskLoop):

    formal_name = HTTP_MODULE_LOOP

    def __init__(self, schedule, args=(), kwargs=None, outbound_queue=None):
        super().__init__(schedule=schedule, callable_=http_impl, args=args, kwargs=kwargs,
                         outbound_queue=outbound_queue)
