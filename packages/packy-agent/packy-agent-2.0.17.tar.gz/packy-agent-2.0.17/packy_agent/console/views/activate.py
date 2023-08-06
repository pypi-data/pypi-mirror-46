import logging

import flask
from flask.views import MethodView
from flask import redirect, url_for, flash, render_template

from packy_agent.console.forms.activate import ActivateForm
from packy_agent.console.forms.activate_extra import ActivateExtraForm
from packy_agent.console.views.base import smart_redirect
from packy_agent.exceptions import AuthenticationError, ValidationError
from packy_agent.domain_logic.managers.install_and_upgrade import install_and_upgrade_manager
from packy_agent.utils.auth import set_authentication_cookie, not_activated
from packy_agent.clients.packy_server import get_inactive_agents

logger = logging.getLogger(__name__)


class ActivateView(MethodView):

    @not_activated
    def get(self):
        return flask.render_template('activate.html', form=ActivateForm())

    @not_activated
    def post(self):
        form = ActivateForm()
        if form.validate():
            email = form.email.data
            password = form.password.data

            try:
                agent_id = None
                agents = get_inactive_agents(email, password)
                if agents:
                    # There inactivate agents, so we have to ask if we should reactivate one of them
                    form = ActivateExtraForm(email=email, password=password)
                    agent_choices = tuple((str(id_), name) for id_, name in agents.items())
                    form.agent.choices += agent_choices

                    if form.validate():
                        if form.agent.data != 'new':
                            # User to reactivate one of the agents, let's take its id
                            agent_id = int(form.agent.data)
                            if agent_id not in agents:
                                flask.flash('Invalid agent')
                                return redirect(url_for('activation_failure'))
                    elif form.extra.data == 'yes':
                        # Data did not pass validation and we need to render errors on extra form
                        return render_template('activate_extra.html', form=form)
                    else:
                        # Data did not pass validation because `activate.html` was actually
                        # submitted, so return extra form with a list of inactive agents
                        form = ActivateExtraForm(email=email, password=password)
                        form.agent.choices += agent_choices
                        return render_template('activate_extra.html', form=form)

                # Otherwise reactivate or create or agent
                install_and_upgrade_manager.activate(email, password, agent_id=agent_id)

            except AuthenticationError:
                flash('Not authenticated (invalid credentials)')
                return flask.redirect(flask.url_for('activation_failure'))
            except ValidationError as ex:
                flash(str(ex))
                return flask.redirect(flask.url_for('activation_failure'))
            except Exception:
                logger.exception('Error during activation')
                flash('Error during activation')
                return redirect(flask.url_for('activation_failure'))

            set_authentication_cookie()
            return smart_redirect('success', 'index', button_text='Continue')

        return render_template('activate.html', form=form)


class ActivationFailureView(MethodView):

    def get(self):
        return render_template('activation_failure.html')
