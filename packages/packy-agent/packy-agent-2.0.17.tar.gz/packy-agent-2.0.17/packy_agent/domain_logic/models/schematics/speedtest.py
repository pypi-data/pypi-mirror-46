from schematics import types

from packy_agent.domain_logic.models.schematics.base import BaseMeasurement


class SpeedtestModuleMeasurement(BaseMeasurement):
    target = types.IntType(required=True)
    upload_speed = types.FloatType()
    download_speed = types.FloatType()
    ping = types.FloatType()
