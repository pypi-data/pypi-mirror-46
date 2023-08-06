import logging
import logging.config

import gevent

from packy_agent.configuration.settings import settings


DEFAULT_LOGGING_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'


logger = logging.getLogger(__name__)


def configure_logging_basic(level=logging.DEBUG):
    logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, level=level)


def configure_logging(basic_level=logging.DEBUG):
    configure_logging_basic(level=basic_level)
    logger.info('Applied basic logging configuration first to debug logging configuration '
                'issues themselves')
    logging.config.dictConfig(settings.get_logging())
    logging.getLogger().setLevel(settings.get_log_level())
    logger.info('FINISHED applying logging configuration')


class GeventFilter(logging.Filter):

    def filter(self, record):
        record.greenlet_id = id(gevent.getcurrent()) % 100
        return True
