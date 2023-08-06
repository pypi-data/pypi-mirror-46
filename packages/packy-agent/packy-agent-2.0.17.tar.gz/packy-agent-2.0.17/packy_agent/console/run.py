import logging

from packy_agent.console.app import get_app
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging_basic
from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.constants import CONSOLE_COMPONENT


def entry():
    settings.set_runtime('component', CONSOLE_COMPONENT)

    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)

    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--http-port', '--port', type=int, default=settings.get_console_http_port())
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    app = get_app(args)
    app.run(host=args.host, port=settings.get_console_http_port(), debug=args.debug)


if __name__ == '__main__':
    entry()
