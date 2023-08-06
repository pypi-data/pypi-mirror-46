import functools
from flask import session, redirect, request, url_for
from packy_agent.configuration.settings import settings


def is_activated():
    return settings.is_activated()


def is_authenticated():
    agent_key = session.get('agent_key')
    if agent_key is not None:
        return settings.get_agent_key() == agent_key
    return False


def set_authentication_cookie():
    agent_key = settings.get_agent_key()
    if agent_key is not None:
        session['agent_key'] = agent_key


def login():
    set_authentication_cookie()


def logout():
    session.pop('agent_key', None)


def not_activated(func_or_method):
    @functools.wraps(func_or_method)
    def wrapper(*args, **kwargs):
        if is_activated():
            return redirect(url_for('index'))

        return func_or_method(*args, **kwargs)

    return wrapper


def activation_and_authentication_required(func_or_method):
    @functools.wraps(func_or_method)
    def wrapper(*args, **kwargs):
        if not is_activated():
            return redirect(url_for('activate'))
        elif not is_authenticated():
            return redirect(url_for('login') + '?next=' + request.path)
        else:
            return func_or_method(*args, **kwargs)

    return wrapper


def activation_required(func_or_method):
    @functools.wraps(func_or_method)
    def wrapper(*args, **kwargs):
        if not is_activated():
            return redirect(url_for('activate'))
        else:
            return func_or_method(*args, **kwargs)

    return wrapper
