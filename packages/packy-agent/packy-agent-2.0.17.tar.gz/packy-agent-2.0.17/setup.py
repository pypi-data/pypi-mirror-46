from setuptools import setup

version = __import__('packy_agent').__version__

setup(
    name='packy-agent',
    version=version,
    description='Packy Agent',
    packages=['packy_agent'],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'packy-agent-console = packy_agent.console.run:entry',
            'packy-agent-watchdog = packy_agent.watchdog.run:entry',
            'packy-agent-worker = packy_agent.worker.run:entry',
            'packy-agent-settings = packy_agent.cli.settings:entry',
            'packy-agent-activate = packy_agent.cli.activate:entry',
            'packy-agent-welcome = packy_agent.cli.welcome:entry',
            'packy-agent-ping = packy_agent.cli.ping:entry',
            'packy-agent-traceroute = packy_agent.cli.traceroute:entry',
            'packy-agent-http = packy_agent.cli.http:entry',
            'packy-agent-set-dhcp = packy_agent.cli.set_dhcp:entry',
            'packy-agent-version = packy_agent.cli.version:entry',
            'packy-agent-migrate1to2 = packy_agent.cli.migrate1to2:entry',
        ]
    }
)
