from urllib.parse import urlencode

import flask
from werkzeug.routing import BuildError


def get_url(endpoint):
    try:
        return flask.url_for(endpoint)
    except BuildError:
        return endpoint


def smart_redirect(endpoint, back_endpoint, button_text='Back'):
    back = urlencode({
        'back_url': get_url(back_endpoint),
        'button_text': button_text,
    })
    url = get_url(endpoint) + '?' + back
    return flask.redirect(url)
