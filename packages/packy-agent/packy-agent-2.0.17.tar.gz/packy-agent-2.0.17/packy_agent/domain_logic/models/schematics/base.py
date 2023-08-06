import json
import time

from schematics import Model, types


class CustomSchematicsModel(Model):

    def to_json(self, *args, **kwargs):
        json_kwargs = kwargs.pop('json_kwargs', {})
        return json.dumps(self.to_primitive(*args, **kwargs), **json_kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.to_primitive()!r})'


class BaseMeasurement(CustomSchematicsModel):
    ts = types.IntType(default=lambda: int(time.time()), required=True)
