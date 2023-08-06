import time
import logging

from sqlalchemy import create_engine, delete, select, func

from packy_agent.configuration.settings import settings
from packy_agent.utils.container import container
from packy_agent.utils.gevent import database_locks
from packy_agent.domain_logic.models.sqlalchemy.base import Session
from packy_agent.domain_logic.models.sqlalchemy.measurement import Measurement
from packy_agent.domain_logic.models.schematics.ping import PingModuleMeasurement
from packy_agent.domain_logic.models.schematics.traceroute import TraceModuleMeasurement
from packy_agent.domain_logic.models.schematics.speedtest import SpeedtestModuleMeasurement
from packy_agent.domain_logic.models.schematics.http import HTTPModuleMeasurement
from packy_agent.constants import ErrorSide

TYPE_MAP = {
    PingModuleMeasurement: 1,
    TraceModuleMeasurement: 2,
    SpeedtestModuleMeasurement: 3,
    HTTPModuleMeasurement: 4,
}

REVERSE_TYPE_MAP = {v: k for k, v in TYPE_MAP.items()}
assert len(TYPE_MAP) == len(REVERSE_TYPE_MAP)

logger = logging.getLogger(__name__)


class LocalStorage:

    def __init__(self):
        self._engine = None

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine(settings.get_database_url())

        return self._engine

    def save_measurement(self, instance):
        # TODO(dmu) LOW: Get database url from self.engine
        with database_locks[settings.get_database_url()]:
            with Session(self.engine) as session:
                session.add(
                    Measurement(
                        measurement_type=TYPE_MAP[instance.__class__],
                        value=instance.to_json(json_kwargs={'separators': (',', ':')}).encode()
                    ))

    def get_remaining_measurements(self, measurement_type=None, limit=100):
        with Session(self.engine) as session:
            query = session.query(Measurement).filter_by(submitted_at_ts=None)
            if measurement_type is not None:
                query = query.filter_by(measurement_type=measurement_type)
            return query.order_by(Measurement.created_at_ts)[:limit]

    def mark_measurement_as_submitted(self, id_):
        logger.debug(f'MARKING measurement as submitted: id = {id_!r}')
        with Session(self.engine) as session:
            session.query(Measurement).filter_by(id=id_).update(
                values={'submitted_at_ts': time.time()})
        logger.debug(f'MARKED measurement as submitted: id = {id_!r}')

    def save_measurement_error(self, id_, error_side, error_message=None, error_at_ts=None):
        logger.debug(f'SAVING measurement error: id = {id_!r}, side = {error_side}, '
                     f'error_message = {error_message!r}, error_at_ts = {error_at_ts!r} ...')

        values = {
            'error_side': error_side,
            'error_at_ts': error_at_ts or time.time(),
            'error_message': error_message
        }
        with Session(self.engine) as session:
            session.query(Measurement).filter_by(id=id_).update(values=values)

        logger.debug(f'SAVED measurement error: id = {id_!r}, side = {error_side}, '
                     f'error_message = {error_message!r}, error_at_ts = {error_at_ts!r}')

    def purge_measurements(self, filter_args=None, filter_by_kwargs=None):
        with Session(self.engine) as session:
            qs = session.query(Measurement)
            if filter_args:
                qs = qs.filter(*filter_args)

            if filter_by_kwargs:
                qs = qs.filter_by(**filter_by_kwargs)

            deleted_count = qs.delete()

        if deleted_count:
            logger.debug('STARTED VACUUM')
            self.engine.execute('VACUUM')
            logger.debug('FINISHED VACUUM')

        return deleted_count

    def purge_unsubmitted_measurements(self, number_of_records=None):
        if number_of_records:
            inner_query = select(
                [Measurement.id]).order_by(Measurement.created_at_ts).limit(number_of_records)
            query = delete(Measurement).where(Measurement.id.in_(inner_query))
        else:
            query = delete(Measurement)

        with Session(self.engine) as session:
            return session.execute(query).rowcount

    def purge_submitted_measurements(self):
        logger.debug('Purging submitted measurements...')
        deleted_counter = self.purge_measurements(
            filter_args=(Measurement.submitted_at_ts.isnot(None),))
        logger.debug('Purged submitted measurements: %s', deleted_counter)

        return deleted_counter

    def purge_failed_measurements(self):
        logger.debug('Purging failed measurements...')
        created_at_threshold_ts = (
            time.time() - settings.get_worker_client_side_failed_submissions_timeout_seconds())

        deleted_counter = self.purge_measurements(
            filter_args=(Measurement.error_side == ErrorSide.CLIENT.value,
                         Measurement.created_at_ts <= created_at_threshold_ts))
        logger.debug('Purged failed measurements: %s', deleted_counter)

        return deleted_counter

    def get_measurements_number(self):
        with Session(self.engine) as session:
            return session.query(func.count('*')).select_from(Measurement).scalar()


def get_local_storage():
    local_storage = getattr(container, 'local_storage', None)
    if not local_storage:
        container.local_storage = local_storage = LocalStorage()

    return local_storage
