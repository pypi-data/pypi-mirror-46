Version 2.0.17
--------------
* FIX: Installation bug because of missing croniter dependency
* UPGRADE: Upgrade supervisor to v4.0.2 so now installable from PyPI

Version 2.0.16
--------------
* IMPROVEMENT: Do not try to submit measurements if submission period is over (leave them for the next period)
* FIX: Fixed incorrect calculation of RTT because of interference of parallel traceroute probes (again)
* FIX: Log only one warning message in case of missed schedule for a task
* FIX: Ping timeout reduced to 2 seconds
* FIX: Debug page actually shows tails of log files
* FIX: Docker version installable for `test01` and other non-production environments
* FIX: Fixed unittests
* UPGRADE: Upgraded wampy to v0.9.21

Version 2.0.15
--------------
* FIX: Cache settings from server for longer

Version 2.0.14
--------------
* FEATURE: Report load average and CPU usage for performance degradation warnings
* IMPROVEMENT: More feasible calculation of "stale on" period
* FIX: Fixed bug that made traceroute take much more time to finish

Version 2.0.13
--------------
* IMPROVEMENT: Do not run VACUUM if no measurements were purged
* IMPROVEMENT: Worker logs warnings to Sentry by default
* FIX: Fixed incorrect calculation of RTT because of interference of parallel traceroute probes
* UPGRADE: Upgraded `sentry-sdk` to v0.6.6

Version 2.0.12
--------------
* IMPROVEMENT: Do not reset network data usage sequence sent server if agent restarts
* CHANGE: Purge failed Agent side measurement submissions in one hour (configurable)

Version 2.0.11
--------------
* FIX: If Packy Server is not available then Packy Agent cumulatively sends network usage

Version 2.0.10
--------------
* FEATURE: Upgrade logging to Packy Server
* FIX: Fix for submitting unsuccessful HTTP measurement
* FIX: Fix Worker dies if settings are not available (not even previously cached)

Version 2.0.9
-------------
* CHANGE: If Speedtest server is not configured (yet) Worker does not raise exception
* CHANGE: If URL (for HTTP module task) is not configured (yet) Worker does not raise exception

Version 2.0.8
-------------
* FIX: If Worker was stopped on purpose then Watchdog should not start it
* FIX: Fix upgrade

Version 2.0.7
-------------
* FIX: Installation fixes

Version 2.0.6
-------------
* FEATURE: Restart agent once a day to defend from potential memory leaks
* FEATURE: Watchdog checks Console health and restarts it if needed (including nginx)
* FEATURE: Watchdog reports on exhausting disk space
* FEATURE: "Reset and reboot" button on "Network Configuration" form if configuration was changed
* IMPROVEMENT: Docker images size reduced from 700Mb to 235Mb (by 66%)
* IMPROVEMENT: Extra measures to avoid too often restarts and reboots by Watchdog
* IMPROVEMENT: If user changes IP address in network configuration then `Back` button redirects
  to the new address
* FIX: Non-printable characters in logs are ignored for `/debug/` instead showing empty log

Version 2.0.5
-------------
* IMPROVEMENT: Added 2Gb swapfile for Raspberry Pi and Orange Pi platforms
* IMPROVEMENT: More details on platform reporting for Sentry
* IMPROVEMENT: Improved greenlet-multitasking safety
* CHANGE: Do not distinguish point versions on of Raspbian since they are bug fixes
* FIX: Fix for handling too many agents error during agent activation

Version 2.0.4
-------------
* IMPROVEMENT: More accurate RTT measurement in case of concurrent traceroute running at the same time
* IMPROVEMENT: Does not store empty hops for UDP and ICMP traceroute in case of unreachable host
* IMPROVEMENT: Faster ICMP traceroute in case of unreachable host
* BACKPORTED: Send more detailed information about platform in User-Agent
* FIX: Concurrent trace (and ping) module tasks compatibility with gevent
* FIX: Trace module better validates host replies structure to avoid exceptions
* FIX: Fixed packy-agent-ping, packy-agent-traceroute and packy-agent-http CLI tools
* FIX: Packy logo size fix for Packy Agent Console

Version 2.0.3
-------------
* FIX: Fix upgrade from Console and Worker

Version 2.0.2
-------------
* FIX: SSL support for connection to Packy Communication on `test01` and `production`

Version 2.0.1
-------------
* IMPROVEMENT: More automated build and deploy of Python package and Docker image
* FIX: Alpine support bug fix

Version 2.0.0
-------------
* FEATURE: Measurements are no longer lost if Packy Server is down. Collected and submitted later
* FEATURE: Much more sophisticated Watchdog: properly handles unavailabilty of Packy Server, checks
  supervisor program status for Worker, checks OS-level process status, check Worker process
  status over HTTP, checks actual workflow and data processing inside Worker, less aggressive
  reboot policy, sentry messages throttling
* FEATURE: Worker status available over HTTP (includes stats on Worker internal loops activity)
* FEATURE: Worker tasks periods are configurable with cron-like syntax
* FEATURE: packy-agent-settings CLI tool
* FEATURE: Refresh tokens support
* IMPROVEMENT: Celery-based architecture is replaced with WAMP(Crossbar)-based architecture:
  easier to support, better source code maintainability, less points of failure, less built-in
  limitations, better server-side scalability, less RAM consumption, less network data usage
* IMPROVEMENT (security): Agent with its own access token can access to only what belongs to it
* IMPROVEMENT: More flexible settings subsystem: introduction sqlite3-based key value storage,
  multilayer settings with dictionary key override (local RAM, command line, environment variables,
  server, cached, local storage, settings file,  defaults)
* IMPROVEMENT: Better naming and structure of agent settings
* IMPROVEMENT: Officially supported platforms: Armbian Bionic mainline kernel 4.14.y,
  Raspbian Stretch Lite October 2018, Ubuntu Server 16.04 LTS, Ubuntu Server 18.04 LTS,
  Docker (guest: Alpine 3.8.1)
* IMPROVEMENT: Migrated to pipenv
* IMPROVEMENT: Introduced pyenv
* IMPROVEMENT: Manual tests (Behave/BDD-based)
* IMPROVEMENT: Unittests with code coverage calculation
* IMPROVEMENT: Code quality and refactoring (better naming and more maintainable structure)
* UPGRADE: Upgraded and migrated to Python 3.7.1
* UPGRADE: Upgraded to Alpine 3.8
* CHANGE: Packy Agent Control Server renamed to Packy Agent Console
* CHANGE: The component that actually runs measuring tasks is now named Packy Agent Worker
* PORTED: Ping module support
* PORTED: Trace (traceroute) module support
* PORTED: Speedtest module support
* PORTED: HTTP module support
* PORTED: Management features of Packy Agent Worker: update settings (reload), restart, reboot,
  heartbeat, upgrade
* PORTED: All features of Packy Agent Console: activation, deactivation, login, logout,
  index (status) page,  network configuration (with refactoring), reset (with refactoring),
  start/stop/restart/reboot, upgrade, debug page
* PORTED: Packy Agent Watchdog
* PORTED: packy-agent-activate CLI tool
* PORTED: packy-agent-welcome CLI tool
* PORTED: packy-agent-traceroute CLI tool
* PORTED: Not activated agent notifies server with its Console URL for activation
* PORTED: Integration with Sentry (also migrated to sentry-sdk from legacy raven library)
* PORTED: Ansible-based installation/upgrade scripts
* PORTED: Build and deploy automation
* PORTED: Smooth upgrade from previous version

Version 0.3.14
--------------
* WORKAROUND: Workaround for UDP trace of unreachable hosts

Version 0.3.13
--------------
* IMPROVEMENT: Send Alpine version in User-Agent

Version 0.3.12
--------------
* IMPROVEMENT: Send more detailed information about platform in User-Agent

Version 0.3.11
--------------
* FIX: Reboot for docker version

Version 0.3.10
--------------
* IMPROVEMENT: Update `server_base_url` of Control Server on config update

Version 0.3.9
-------------
* FIX: Upgrade to pip 10.0.1, virtualenv 16.0.0 and pycurl 7.43.0.2 to avoid Segmentation Faults
  during installation/upgrade

Version 0.3.8
-------------
* FEATURE: Report being on Docker to Sentry
* FIX: libcurl ImportError bug fix

Version 0.3.7
-------------
* FEATURE: Logging to Sentry
* IMPROVEMENT: Gevent dependency removed

Version 0.3.6
-------------
* FIX: Fixed ICMP traceroute

Version 0.3.5.1
---------------
* FIX: Fixed ping of unresolvable host

Version 0.3.4.1
---------------
* FEATURE: Concurrent upgrade detection and displayed upgrading status
* IMPROVEMENT: Self-healing reliable Ansible-based agent upgrade

Version 0.3.3.1
---------------
* FEATURE: Asymmetric traceroute path detection
* FEATURE: Deactivate/reactive agent

Version 0.3.2
-------------
* FEATURE: Support for ping interval
* IMPROVEMENT: Task results are no longer collected in RabbitMQ
* CHANGE: HTTP module redirect allows up to 50 redirects

Version 0.3.1
-------------
* FEATURE: UDP traceroute implementation
* FEATURE: Support for traceroute method and parallelism options
* FEATURE: CLI for ping: sudo python -m packy_agent.modules.ping.cli --help
* IMPROVEMENT: Prevented parallel execution of the same module task
* IMPROVEMENT: ICMP traceroute fully reimplemented with various bug fixes including interference
  with ping
* IMPROVEMENT: Ping fully reimplemented with various bug fixes including interference with
  traceroute
* IMPROVEMENT: Parallel traceroute implementation without gevent
* FIX: Traceroute is actually using `packet_size` setting now

Version 0.3.0
-------------
* CHANGE: Moved to public PyPI repository

Version 0.2.21
--------------
* FIX: Packy Server is requested with timeout
* UPGRADE: Upgraded to requests==2.18.4, idna==2.6, urllib3==1.22

Version 0.2.20
--------------
* UPGRADE: Upgraded Celery to 4.1.0

Version 0.2.19
--------------
* FIX: Clean up for traceroute results submission

Version 0.2.18
--------------
* FEATURE: Support for "Simplified agent deployment"

Version 0.2.17
--------------
* IMPROVEMENT: Restrict highest upgradable version from server
* IMPROVEMENT: Use API v2 to get agent configuration

Version 0.2.16
--------------
* FIX: Fix for getting uptime inside docker container
* CHANGE: Libraries upgrade: `amqp==2.2.2`, `billiard==3.5.0.3`, `kombu==4.1.0`,
  `speedtest-cli==1.0.7`, `supervisor==3.3.3`

Version 0.2.15
--------------
* FEATURE: Agent data usage monitoring
* CHANGE: API v2 is used for measurements submission

Version 0.2.14
--------------
* IMPROVEMENT: New options for `python -m packy_agent.cli.configure`: `--control-server-port 80`,
  `--remove-nginx-default-landing`
* FIX: Bug fixes

Version 0.2.13
--------------
* IMPROVEMENT: Log rotation for Packy Agent, Control Server and Watchdog
* IMPROVEMENT: Better handling log directories creation with Armbian's log2ram service
* CHANGE: Task chaining removed for Ping, Trace and Speedtest modules

Version 0.2.12
--------------
* FEATURE: HTTP module
* FEATURE: Update configuration file from server on agent start
* FIX: Bug fixes

Version 0.2.11
--------------
* FIX: Speedtest bug work-around

Version 0.2.10
--------------
* FEATURE: Command line activation via `packy-agent-activate` tool
* FEATURE: `install` task with explicit version (to be used for downgrades and testing)
* IMPROVEMENT: Agent activation is done in a single HTTP request (this should improve activate
  success on poor networks and also reduce number of orphan agents)
* IMPROVEMENT: `upgrade`/`upgrade_self` task upgrades not only Python Package, but also upgrades
  and configures infrastructure components like supervisord, uWSGI and nginx
* CHANGE: `update_self` renamed to `upgrade`

Version 0.2.9
-------------
* IMPROVEMENT: Most of the installation script is moved into Packy Agent and written in Python
* IMPROVEMENT: `null` is sent instead of '* * *' for unknown hop
* FIX: Installation script fix for upgrade: `service packy start/stop` fix (added systemd support)
* FIX: Watchdog loop wait bug fix

Version 0.2.8
-------------
* IMPROVEMENT: Support of network configuration for Armbian along with better OS flavor detection
* FEATURE: Orange Pi Zero setup instruction
* FIX: Fix for "Reset Activation" feature

Version 0.2.7
-------------
* IMPROVEMENT: uWSGI is put behind nginx

Version 0.2.6.1
---------------
* FIX: Agent activation bug fix

Version 0.2.6
-------------
* FEATURE: Watchdog
* FEATURE: Logout for Control Server
* FIX: Time for measurements is sent in UTC

Version 0.2.5
-------------
* FEATURE: Control Server authentication
* FEATURE: Support for `version`, `ip_address` and `public_ip_address` update for agents
           on heartbeat
* FEATURE: Restart task

Version 0.2.4
-------------
* FEATURE: New in Control Server:

    - Beagel style UI (the same of for Packy Server) with usability improvements
    - Agent status page
    - Network configuration
    - Agent running state control: start/stop/restart agent (as supervisor program), reboot
    - Version upgrade
    - Reset to default settings: agent activation and network configuration
    - Debug information (in debug mode): logs tail and configuration files

* FEATURE: Support for installation directly onto operating system: creation of directories,
  generation of supervisor configuration file and init.d script
* FEATURE: Support for token expiration (required because we no longer generate a new token on each
  task run)
* FEATURE: Support for running Configuration Server and Packy Agent with supervisord in development
  environment
* IMPROVEMENT: Running Control Server with uWSGI
* IMPROVEMENT: Celery (Packy Agent) exists with appropriate message if Agent has not been activated
* IMPROVEMENT: Improved error reporting on agent activation failure
* IMPROVEMENT/FIX: Bootstrap server does not ask for activation if agent has already been activated
* IMPROVEMENT/FIX: Refactoring of configuration file management: avoid rereading up to date file,
  atomic file writes, decoupled configuration of boostrap server, agent, flask, celery,
  reads/writes to configuration files are encapsulated in classes
* FIX: New token is no longer generates a new token on each task run (this were polluting
  Packy Server database with waste token records)
* FIX: Small changes: using floats instead of decimals for measurements

Version 0.2.3
-------------
* Improved `README.rst` for running Packy Agent in development mode with root privileges
* Packy Server compatibility changes

Version 0.2.2
-------------
* Reliable online status support
* Compatibility with Packy Server v0.0.8 and later

Version 0.2.1
-------------
* Traceroute is fixed and refactored: performance increase (15-20 seconds per task), bug fix
* Speedtest task is fixed with improvements: `speedtest-cli` is installed as dependency and
  access via Python API instead of running a subprocess, bug fixes
* Improved logging for Bootstrap Server

Version 0.2.0
-------------
* Dockerization (got rid of in-house tar packaging)
* update_self works via private PyPI (got rid of rsync)
* Bootstrap Server (Flask implementation) with improved error reporting
* Configuration files refactoring

Version 0.0.1
-------------
* Python packaging
* Configurable tasks name prefix
* Configuration files refactoring and introduction of YAML-configuration files
* Created `PackyServerClient`
* `python -m packy_agent.cli.register_agent` command (refactored from `generate_key`)
* New `python -m packy_agent.cli.get_bundle_config` command
