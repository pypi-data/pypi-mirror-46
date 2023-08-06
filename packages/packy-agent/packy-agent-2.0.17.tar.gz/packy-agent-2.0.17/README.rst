Development
===========

Initial installation
++++++++++++++++++++

#. Install prerequisites::

    # TODO(dmu) LOW: Which of them I actually do need to have installed?
    sudo apt-get install python-dev build-essential pkg-config python-pip
    sudo apt-get install libssl-dev libffi-dev libsasl2-dev liblz4-dev
    sudo apt-get install git

#. Fork `<https://bitbucket.org/samnz_/packy-agent>`_ repository

#. Clone forked repository (replace <username> with your bitbicket account name)::

    git clone git@bitbucket.org:<username>/packy-agent.git
    cd packy-agent

#. [if you have configured it globally] Configure git::

    git config user.name 'Firstname Lastname'
    git config user.email 'youremail@youremail_domain.com'

#. Install and configure `pyenv` according to https://github.com/pyenv/pyenv#basic-github-checkout
#. Install Python 3.7.1::

    pyenv install 3.7.1

#. Install `pipenv`::

    pip install --user pipenv==2018.11.26

#. Create local configuration file::

    mkdir local

    export PACKY_AGENT_SETTINGS_FILENAME=$PWD/local/packy-agent-settings.yaml

    cat << EOF > $PACKY_AGENT_SETTINGS_FILENAME
    key_value_storage_filename: $PWD/local/packy-agent.sqlite3
    reboot_enabled: false
    upgrade_enabled: false
    vendored_hardware: true  # for testing purposes
    network_configuration_enabled: false
    server_base_url: http://127.0.0.1:8000/
    debug_mode: true

    supervisor:
      configuration_filename: $PWD/local/etc/packy-supervisord.conf
      log_filename: $PWD/local/var/log/packy/supervisor/supervisor.log
      run_directory: $PWD/local/var/run/packy/supervisor

    console:
      uwsgi:
        configuration_filename: $PWD/local/etc/packy-uwsgi.conf
        pid_filename: $PWD/local/var/run/packy/uwsgi/pid

      stdout_log_filename: $PWD/local/var/log/packy/console/standard.log
      stderr_log_filename: $PWD/local/var/log/packy/console/error.log
      version_dump_filename: $PWD/local/etc/packy-agent-console-version

    worker:
      stdout_log_filename: $PWD/local/var/log/packy/console/standard.log
      stderr_log_filename: $PWD/local/var/log/packy/console/error.log
      version_dump_filename: $PWD/local/etc/packy-agent-worker-version

    watchdog:
      stdout_log_filename: $PWD/local/var/log/packy/watchdog/standard.log
      stderr_log_filename: $PWD/local/var/log/packy/watchdog/error.log
      version_dump_filename: $PWD/local/etc/packy-agent-watchdog-version

    log_level: DEBUG
    logging:
      formatters:
        standard:
          format: '%(asctime)s %(levelname)s %(message)s'
      loggers:
        packy_agent.domain_logic.modules:
          level: ERROR
          propogate: true
        packy_agent.configuration.sources.base:
          level: ERROR
          propogate: true
        sqlalchemy.engine:
          level: DEBUG
    EOF

Upgrade
+++++++

#. Change to this repo root directory::

    cd packy-agent

#. Create virtualenv with all required dependencies::

    pipenv install --dev

#. Switch to virtualenv::

    pipenv shell

#. Create directories and configuration files::

    export PACKY_AGENT_SETTINGS_FILENAME=$PWD/local/packy-agent-settings.yaml
    # TODO(dmu) HIGH: This may overwrite configuration files. Fix it.
    ANSIBLE_NOCOWS=1 ansible-playbook -i localhost, -c local packy_agent/scripts/deploy_devenv.yaml

#. Upgrade Packy Agent in development mode::

    pip install -e . (or maybe `pipenv install -e .`)

#. Run migrations::

    alembic -c ./packy_agent/configuration/alembic.ini upgrade head

Run
+++

#. Switch to virtualenv::

    pipenv shell

#. Set envvar to point to configuration file::

    export PACKY_AGENT_SETTINGS_FILENAME=$PWD/local/packy-agent-settings.yaml

#. Run migrations::

    alembic -c ./packy_agent/configuration/alembic.ini upgrade head

#. Run Packy Agent Worker::

    sudo -E `which python` -m packy_agent.worker.run --log-level DEBUG

#. Run Packy Agent Console::

    sudo -E `which python` -m packy_agent.console.run --debug

#. Run Packy Agent Watchdog::

    sudo -E `which python` -m packy_agent.watchdog.run --log-level DEBUG

#. Alternatively run with Supervisor::

    sudo -E `which supervisord` --nodaemon -c ./local/etc/packy-supervisord.conf

Run tests
+++++++++

#. Switch to virtualenv::

    pipenv shell

#. Set envvar to point to configuration file::

    export PACKY_AGENT_SETTINGS_FILENAME=$PWD/local/packy-agent-settings.yaml

#. Run unittests::

    sudo -E `which pytest` --cov=packy_agent --cov-report html -p no:warnings --run-slow ./packy_agent

#. Run manual tests::

    behave manual_tests/

Publish package for testing
+++++++++++++++++++++++++++

#. Build and publish to private PyPI::

    pipenv shell
    ./deploy-scripts/upload-dev.sh

Production
==========

Build
+++++

Build Python Source Distribution package
----------------------------------------

#. Install and configure `pyenv` according to https://github.com/pyenv/pyenv#basic-github-checkout
#. Install Python 3.7.1::

    pyenv install 3.7.1

#. Install `pipenv`::

    pip install --user pipenv

#. Create virtualenv with all required dependencies::

    pipenv install --dev

#. Switch to virtualenv::

    pipenv shell

#. Build and publish Python Source Distribution::

    ./deploy-scripts/upload-python-package.sh
    # For development use: ./deploy-scripts/upload-python-package-dev.sh

Build Docker image
------------------

#. Build Python Source Distribution as described in `Build Python Source distribution package`_
#. Make sure proper version of Packy Server is deployed
#. Build Docker image::

    ./deploy-scripts/build-docker-image.sh https://dashboard.packy.io
    # or ./deploy-scripts/build-docker-image.sh https://test01.packy.io

#. Upload Docker image to registry::

    ./deploy-scripts/upload-docker-image.sh

Install / run
+++++++++++++

On Operating System directly
----------------------------

#. Download and run installation script::

    export PACKY_SERVER_BASE_URL=https://dashboard.packy.io
    # Example 1 for dev env: export PACKY_SERVER_BASE_URL=http://192.168.1.231:8000
    # Example 2 for dev env: export PACKY_SERVER_BASE_URL=http://192.168.1.45:8000
    wget $PACKY_SERVER_BASE_URL/downloads/install-packy-agent.sh -O install-packy-agent.sh && chmod +x install-packy-agent.sh && ./install-packy-agent.sh

On Docker
---------

#. Start docker container::

    # Replace angle brackets (<>) with appropriate values
    ###############################################################################################

    export PACKY_AGENT_VERSION=<version>  # replace <version>

    # For remote image:
    docker login
    export PACKY_IMAGE_NAME=dmugtasimovorg/packy-agent

    # For local image:
    export PACKY_IMAGE_NAME=packy-agent

    # For production:
    docker run -d -p 127.0.0.1:8001:8001 --name packy-agent-container \
        $PACKY_IMAGE_NAME:$PACKY_AGENT_VERSION

    # For testing:
    docker run -i -t --rm -p 127.0.0.1:8001:8001 --name packy-agent-container \
        -e PACKY_SERVER_BASE_URL packy-agent:$PACKY_AGENT_VERSION

#. Register agent at http://127.0.0.1:8001

On Orange Pi
------------

#. Download `Armbian Bionic - mainline kernel 4.14.y` archive from
   https://www.armbian.com/orange-pi-zero/ and uncompress it
#. Flash miscroSD with Etcher:

    #. Install Etcher from https://etcher.io/ and unzip
    #. Run unzipped *.AppImage file
    #. Click "Select image" and select previous downloaded and uncompressed Armbian *.img file
    #. Insert miscroSD card
    #. Click "Flash!"
    #. Enter your password if requested
    #. Wait until flashing is finished
    #. Remove microSD from computer

#. Insert microSD into Orange Pi Zero
#. Power on Orange Pi Zero
#. Connect Orange Pi Zero to wired network
#. Figure out which IP-address was assigned to Orange Pi Zero
   (probably list of DHCP leases on your router may help)
#. Login to Orange Pi Zero::

    ssh root@x.x.x.x
    # enter 1234 as password

#. Change root password and enter other information as prompted
#. Disable armbian-ramlog (because we run out of space too fast)::

    vim /etc/default/armbian-ramlog
    # Change `ENABLED=true` to `ENABLED=false`

#. Upgrade Armbian::

    apt update
    apt upgrade

#. Reboot::

    reboot

#. Login to Orange Pi Zero again::

    ssh root@x.x.x.x

#. [not tested] Add swap file::

    sudo -i
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile

    # Turning on swap file
    swapon /swapfile
    vim /etc/fstab
    # Add the following line
    # /swapfile swap swap defaults 0 0

    # Correcting swappiness to allow longer life for flash memory
    sysctl vm.swappiness=10
    vim /etc/sysctl.conf
    # Add the following line
    # vm.swappiness=10

    reboot

#. Install Packy Agent on Orange Pi Zero:

    #. Download Packy Agent installation script::

        wget https://dashboard.packy.io/downloads/install-packy-agent.sh -O install-packy-agent.sh
        # For development: wget http://192.168.1.231:8000/downloads/install-packy-agent.sh -O install-packy-agent.sh

    #. Set execute bit to `install-packy-agent.sh`::

        chmod +x install-packy-agent.sh

    #. Run installation script::

        sudo mkdir /pip-tmp
        TMPDIR=/pip-tmp PACKY_CONSOLE_HTTP_PORT=80 PACKY_REMOVE_NGINX_DEFAULT_LANDING=True PACKY_IS_VENDORED_HARDWARE=True ./install-packy-agent.sh

    #. [optional] Configure default 192.168.42.42 IP-address for virtual interface
       (will also force to use DHCP for hardware interface)::

        sudo /root/.virtualenvs/packy-agent/bin/packy-agent-set-dhcp --no-reboot --no-backup

On Raspberry Pi
---------------

#. Download `Raspbian Stretch Lite November 2018` from https://www.raspberrypi.org/downloads/raspbian/
#. If it is compressed but not in zip-format then uncompress it
#. Flash miscroSD with Etcher:

    #. Install Etcher from https://etcher.io/ and unzip
    #. Run unzipped *.AppImage file
    #. Click "Select image" and select previous downloaded image (uncompressed if needed)
    #. Insert miscroSD card
    #. Click "Flash!"
    #. Enter your password if requested
    #. Wait until flashing is finished

#. Remove microSD from computer and insert it back
#. Enable SSH server on Raspbian::

    sudo touch <SD card mount root path of boot partition>/ssh

#. Insert microSD into Raspberry Pi
#. Power on Raspberry Pi
#. Connect Raspberry Pi to wired network
#. Figure out which IP-address was assigned to Raspberry Pi
   (probably a list of DHCP leases on your router may help)
#. Login to Raspberry Pi::

    ssh pi@x.x.x.x
    # enter "raspberry" as password (without quotes)

#. Change "pi" user password with `passwd` command
#. Add swap file::

    sudo -i

    # Correct swappiness to allow longer life for flash memory
    sysctl vm.swappiness=10
    nano /etc/sysctl.conf
    # Add the following line
    # vm.swappiness=10

    # Increase on swap file size
    nano /etc/dphys-swapfile
    # Modify to 2Gb
    # CONF_SWAPSIZE=2048

    dphys-swapfile setup
    dphys-swapfile swapon
    exit

#. Upgrade and reboot Raspbian::

    sudo -i
    apt update
    apt upgrade
    reboot

#. Install Packy Agent on Raspberry Pi:

    #. Download Packy Agent installation script::

        wget https://dashboard.packy.io/downloads/install-packy-agent.sh -O install-packy-agent.sh
        # For testing: wget https://test01.packy.io/downloads/install-packy-agent.sh -O install-packy-agent.sh
        # For development: wget http://192.168.1.231:8000/downloads/install-packy-agent.sh -O install-packy-agent.sh

    #. Set execute bit to `install-packy-agent.sh`::

        chmod +x install-packy-agent.sh

    #. Run installation script::

        sudo mkdir /pip-tmp
        TMPDIR=/pip-tmp PACKY_CONSOLE_HTTP_PORT=80 PACKY_REMOVE_NGINX_DEFAULT_LANDING=True PACKY_IS_VENDORED_HARDWARE=True ./install-packy-agent.sh

    #. [optional] Configure default 192.168.42.42 IP-address for virtual interface
       (will also force to use DHCP for hardware interface)::

        sudo /root/.virtualenvs/packy-agent/bin/packy-agent-set-dhcp --no-reboot --no-backup
