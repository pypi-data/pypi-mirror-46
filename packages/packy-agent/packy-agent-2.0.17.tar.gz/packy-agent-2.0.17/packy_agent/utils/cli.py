import argparse

from packy_agent.configuration.settings import settings


def get_base_argument_parser(module=None, kwargs=None, default_log_level=None):
    kwargs = kwargs or {}
    if module:
        kwargs['prog'] = 'python -m {}'.format(module)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     **kwargs)
    parser.add_argument(
        '--log-level', help='Log level',
        default=settings.get_log_level() if default_log_level is None else default_log_level)

    return parser
