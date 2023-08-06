import os
import os.path
import time

import packy_agent


def dump_version(filename, variable_name):
    with open(filename, 'w') as f:
        f.write('{}={}\n'.format(variable_name, packy_agent.__version__))


def is_upgrade_in_progress():
    from packy_agent.configuration.settings import settings
    upgrade_in_progress_lock_filename = settings.get_upgrade_in_progress_lock_filename()
    try:
        mtime = os.path.getmtime(upgrade_in_progress_lock_filename)
    except OSError:
        return False

    upgrade_max_duration_seconds = settings.get_upgrade_max_duration_seconds()
    # We need this check because we want to prohibit automatics restarts/reboots during upgrades,
    # but still want them in case upgrade fails and keeps the lockfile
    return time.time() - mtime < upgrade_max_duration_seconds


def remove_upgrade_in_progress_lock():
    from packy_agent.configuration.settings import settings
    try:
        os.remove(settings.get_upgrade_in_progress_lock_filename())
    except OSError:
        pass
