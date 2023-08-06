from urllib.parse import urljoin

import flask
from flask.views import MethodView

from packy_agent.console.forms.network import NetworkForm
from packy_agent.configuration.settings import settings
from packy_agent.domain_logic.managers.network import network_manager
from packy_agent.domain_logic.managers.reset import reset_manager
from packy_agent.console.views.base import smart_redirect
from packy_agent.utils.auth import activation_and_authentication_required
from packy_agent.console.forms.action import ActionForm


DELAY_SECONDS = 5


class NetworkView(MethodView):

    def get_form_context(self):
        is_network_configuration_supported = network_manager.is_network_configuration_supported()
        network_interface = network_manager.get_configurable_network_interface()

        if is_network_configuration_supported and network_interface:
            form_kwargs = network_manager.get_configuration(network_interface)
            form_kwargs['network_interface'] = network_interface
            form = NetworkForm(**form_kwargs)
        else:
            form = None

        context = {
            'form': form,
            'is_network_configuration_enabled': settings.is_network_configuration_enabled(),
            'network_interface': network_interface,
            'active_menu_item': 'network',
        }
        return context

    @activation_and_authentication_required
    def get(self):
        context = self.get_form_context()
        return flask.render_template('network.html', **context)

    @activation_and_authentication_required
    def post(self):
        action_form = ActionForm()
        if action_form.validate():
            action = action_form.action.data
            if action == 'network_reset':
                if settings.is_network_configuration_enabled():
                    reset_manager.reset_network_configuration(reboot_delay_seconds=DELAY_SECONDS)

                    flask.flash(f'Reboot will start in {DELAY_SECONDS} seconds...')
                    return smart_redirect('success', 'index', button_text='Continue')
                else:
                    flask.flash('Network configuration is not allowed.')
                    return smart_redirect('success', 'network')

        form = NetworkForm()
        if form.validate():

            if form.dhcp.data:
                network_manager.set_dhcp(interface=form.network_interface.data,
                                         reboot_delay_seconds=DELAY_SECONDS)
                back_endpoint = 'network'
            else:
                ip_address = form.ip_address.data
                kwargs = dict(
                    ip_address=ip_address,
                    subnet_mask=form.subnet_mask.data,
                    default_gateway=form.default_gateway.data,
                    interface=form.network_interface.data,
                    reboot_delay_seconds=DELAY_SECONDS,
                )
                if form.name_servers.data:
                    kwargs['name_servers'] = form.name_servers.data.split(',')

                network_manager.set_static_ip_address(**kwargs)

                base_url = settings.get_console_base_url(ip_address)
                back_endpoint = urljoin(base_url, flask.url_for('network'))

            if settings.is_network_configuration_enabled():
                flask.flash(f'Changes will take affect after reboot in {DELAY_SECONDS} seconds...')
            else:
                flask.flash('Dry run. Please, see logs for more information')
                back_endpoint = 'network'  # no changes, so...

            return smart_redirect('success', back_endpoint)

        context = self.get_form_context()
        context['form'] = form
        return flask.render_template('network.html', **context)
