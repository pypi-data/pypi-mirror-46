class Skip(Exception):
    pass


class ImproperlyConfiguredError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class ValidationError(Exception):
    pass


class CoolDown(Exception):
    pass


class NoAccessTokenError(ImproperlyConfiguredError):
    pass


class OutOfPortsError(Exception):
    pass
