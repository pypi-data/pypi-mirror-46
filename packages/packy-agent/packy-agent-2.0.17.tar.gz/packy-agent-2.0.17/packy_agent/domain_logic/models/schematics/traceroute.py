from schematics import types

from packy_agent.domain_logic.models.schematics.base import BaseMeasurement, CustomSchematicsModel


class Hop(CustomSchematicsModel):
    number = types.IntType(min_value=1)

    reply_number = types.IntType(min_value=1)
    ip_address = types.IPv4Type()

    sent = types.IntType(min_value=1, required=True)
    loss_abs = types.IntType(min_value=0, required=True)

    last = types.FloatType(min_value=0)
    best = types.FloatType(min_value=0)
    worst = types.FloatType(min_value=0)
    average = types.FloatType(min_value=0)
    stdev = types.FloatType(min_value=0)


class TraceModuleMeasurement(BaseMeasurement):
    target = types.StringType(required=True)
    packet_size = types.IntType(min_value=0, required=True)
    pings = types.IntType(min_value=1, required=True)
    hops = types.ListType(types.ModelType(Hop))
