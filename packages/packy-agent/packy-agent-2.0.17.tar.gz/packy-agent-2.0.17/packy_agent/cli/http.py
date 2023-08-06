import sys
import logging

from packy_agent.configuration.settings import settings
from packy_agent.utils.cli import get_base_argument_parser
from packy_agent.utils.logging import configure_logging, configure_logging_basic

from packy_agent.domain_logic.modules.http.base import get_http_measurement


def entry():
    configure_logging_basic(logging.WARNING)
    parser = get_base_argument_parser(__loader__.name)

    parser.add_argument('url')
    parser.add_argument('--follow-redirects', action='store_true')

    args = parser.parse_args()
    settings.set_commandline_arguments(vars(args))
    configure_logging(logging.WARNING)

    url = args.url
    print(f'Getting information for {url}')
    print(get_http_measurement(url, follow_redirects=args.follow_redirects).to_json())


if __name__ == '__main__':
    sys.exit(entry())
