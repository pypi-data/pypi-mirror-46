from schematics import types

from packy_agent.domain_logic.models.schematics.base import BaseMeasurement


class PingModuleMeasurement(BaseMeasurement):
    target = types.StringType(required=True)
    packet_size = types.IntType(required=True)
    n_pings = types.IntType(required=True)
    values_ = types.ListType(types.FloatType, serialized_name='values', deserialize_from='values')
