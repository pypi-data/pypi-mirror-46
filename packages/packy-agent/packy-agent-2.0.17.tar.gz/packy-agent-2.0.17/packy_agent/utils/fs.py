import os

from packy_agent.configuration.settings import settings


def get_available_disk_space(path=None):
    path = path or settings.get_database_filename()
    statvfs = os.statvfs(path)
    return statvfs.f_frsize * statvfs.f_bavail
