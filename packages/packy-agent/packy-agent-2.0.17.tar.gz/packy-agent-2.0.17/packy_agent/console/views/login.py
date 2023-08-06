import logging

from requests.exceptions import ConnectionError, HTTPError
import flask
from flask.views import MethodView

from packy_agent.clients.packy_server import get_packy_server_client
from packy_agent.console.forms.login import LoginForm

from packy_agent.utils.auth import set_authentication_cookie, activation_required


logger = logging.getLogger(__name__)


def login_failure():
    return flask.redirect(flask.url_for('login_failure'))


class LoginView(MethodView):

    @activation_required
    def get(self):
        return flask.render_template('login.html', form=LoginForm())

    @activation_required
    def post(self):
        form = LoginForm()
        if form.validate():
            try:
                is_valid = get_packy_server_client().validate_auth(form.email.data, form.password.data)
            except ConnectionError:
                flask.flash('Packy Server is unavailable for authentication. '
                            'Please, try again later')
                return login_failure()
            except HTTPError as ex:
                status_code = ex.response.status_code
                if 400 <= status_code < 500:
                    flask.flash('An error occurred during authentication. '
                                'Please, upgrade Packy Agent and/or try later')
                    return login_failure()
                elif 500 <= status_code < 600:
                    flask.flash('Packy Server is failure during authentication. '
                                'Please, again try later')
                    return login_failure()
                else:
                    raise

            if not is_valid:
                flask.flash('Not authenticated (invalid credentials)')
                return login_failure()

            set_authentication_cookie()
            url = flask.request.args.get('next')
            if not url:
                url = flask.url_for('index')

            return flask.redirect(url)

        return flask.render_template('login.html', form=form)


class LoginFailureView(MethodView):

    def get(self):
        return flask.render_template('login_failure.html')
