import logging
import time
import enum
from collections import defaultdict, deque

from gevent.lock import RLock
from gevent import Greenlet


SWITCH_LOG_MAX_LEN = 3000

logger = logging.getLogger(__name__)
database_locks = defaultdict(RLock)


class SwitchType(enum.Enum):
    IN = 0
    OUT = 1


class CustomGreenlet(Greenlet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.switch_log = deque(maxlen=SWITCH_LOG_MAX_LEN)

    def switch(self, *args, **kwargs):
        # TODO(dmu) HIGH: Implementation should be improved after having this issue resolved:
        #                 https://github.com/gevent/gevent/issues/1343
        # assert not self.switch_log or self.switch_log[-1][0] == SwitchType.OUT.value, 'Switch in without switch out is detected'
        now = time.time()
        if not self.switch_log or self.switch_log[-1][0] == SwitchType.OUT.value:
            self.switch_log.append((SwitchType.IN.value, now))

        return super().switch(*args, **kwargs)

    def switch_out(self):
        # TODO(dmu) HIGH: Implementation should be improved after having this issue resolved:
        #                 https://github.com/gevent/gevent/issues/1343
        # assert self.switch_log, 'Switch out without switch in is detected'
        # assert self.switch_log[-1][0] == SwitchType.IN.value, 'Switch out without switch in is detected'
        now = time.time()
        if self.switch_log and self.switch_log[-1][0] == SwitchType.IN.value:
            self.switch_log.append((SwitchType.OUT.value, now))

    def clear_switch_log(self):
        self.switch_log.clear()

    def get_switch_log_durations(self):
        switch_log_iter = iter(self.switch_log)
        durations = []
        for switch_in_item in switch_log_iter:
            assert switch_in_item[0] == SwitchType.IN.value
            try:
                switch_out_item = next(switch_log_iter)
            except StopIteration:
                break

            assert switch_out_item[0] == SwitchType.OUT.value
            durations.append(switch_out_item[1] - switch_in_item[1])

        return durations
