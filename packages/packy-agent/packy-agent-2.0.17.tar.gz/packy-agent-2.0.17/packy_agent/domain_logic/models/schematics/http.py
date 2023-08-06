from schematics import types

from packy_agent.domain_logic.models.schematics.base import BaseMeasurement


class HTTPModuleMeasurement(BaseMeasurement):
    target = types.StringType(required=True)

    is_success = types.BooleanType(default=True)
    http_status_code = types.IntType()

    namelookup_ms = types.FloatType()
    total_ms = types.FloatType()

    certificate_expiration_dt = types.DateTimeType()
