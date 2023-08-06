import sys
import logging

import yaml
import termcolor

from packy_agent.configuration.settings import settings
from packy_agent.utils.logging import configure_logging, configure_logging_basic
from packy_agent.utils.cli import get_base_argument_parser

LIST_COMMAND = 'list'
SET_COMMAND = 'set'
GET_COMMAND = 'get'
DEL_COMMAND = 'del'
CLEAR_COMMAND = 'clear'

is_a_tty = sys.stdout.isatty()


def print_key_value(key, value, is_shadowed=False):
    yaml_value = yaml.dump(value)
    if yaml_value.endswith('...\n'):
        yaml_value = yaml_value[:-4]

    yaml_value = yaml_value.rstrip('\n')

    text = '{}={}'.format(key, yaml_value)
    if is_shadowed:
        if is_a_tty:
            termcolor.cprint(text, attrs=('dark',))
        else:
            print(f'/ {text} /')
    else:
        print(text)


def list(args):
    all_keys = not getattr(args, 'effective', False)
    known_keys = set()
    for priority, (label, items) in enumerate(settings.labeled_items(), start=1):
        header = f'PRIORITY {priority}: {label}'
        print(header)
        print('=' * len(header))
        for key, value in items:
            is_shadowed = key in known_keys
            if all_keys or not is_shadowed:
                print_key_value(key, value, is_shadowed=is_shadowed)

            known_keys.add(key)

        print()


def set_key(args):
    settings.set(args.key, args.value)


def del_key(args):
    settings.delete(args.key)


def clear(args):
    settings.clear()


def get_value(args):
    key = args.key
    print_key_value(key, settings.get(key, '<NOT SET>'))


COMMAND_TO_FUNCTION_MAP = {
    LIST_COMMAND: list,
    SET_COMMAND: set_key,
    GET_COMMAND: get_value,
    DEL_COMMAND: del_key,
    CLEAR_COMMAND: clear,
}


def entry():
    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)

    subparsers = parser.add_subparsers(title='command', dest='command')
    list_parser = subparsers.add_parser(LIST_COMMAND, help='List all known settings')
    list_parser.add_argument('-e', '--effective', action='store_true')
    get_parser = subparsers.add_parser(GET_COMMAND, help='Get particular setting')
    get_parser.add_argument('key')
    set_parser = subparsers.add_parser(SET_COMMAND, help='Set particular setting (local)')
    set_parser.add_argument('key')
    set_parser.add_argument('value')
    set_parser = subparsers.add_parser(DEL_COMMAND, help='Delete particular setting (local)')
    set_parser.add_argument('key')
    subparsers.add_parser(CLEAR_COMMAND, help='Clear settings (local)')

    args = parser.parse_args()

    settings.set_commandline_arguments(vars(args))
    configure_logging(logging.WARNING)

    # Call function named `args.command` and pass `args` to it
    COMMAND_TO_FUNCTION_MAP[args.command or LIST_COMMAND](args)


if __name__ == '__main__':
    sys.exit(entry())
