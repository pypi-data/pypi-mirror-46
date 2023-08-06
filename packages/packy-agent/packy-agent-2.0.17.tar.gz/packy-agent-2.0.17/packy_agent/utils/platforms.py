import os
import distro


LINUX_MINT = 'linuxmint'
UBUNTU = 'ubuntu'
RASPBIAN = 'raspbian'
ALPINE = 'alpine'

PRETTY_NAMES = {
    LINUX_MINT: 'Linux Mint',
    UBUNTU: 'Ubuntu',
    RASPBIAN: 'Raspbian',
    ALPINE: 'Alpine',
}

LINUX_MINT_18_1 = (LINUX_MINT, '18.1')
UBUNTU_16_04 = (UBUNTU, '16.04')
UBUNTU_18_04 = (UBUNTU, '18.04')
RASPBIAN_9 = (RASPBIAN, '9')


def get_os_id_and_version():
    distro_id = distro.id()
    version_parts = distro.version_parts(best=True)
    if distro_id == RASPBIAN:
        version = version_parts[0]
    else:
        version = '.'.join(version_parts[:2])

    return distro_id, version


def is_inside_docker_container():
    return os.path.isfile('/.dockerenv')


def get_platform():
    platform = distro.name(pretty=True) or 'unidentified'
    if is_inside_docker_container():
        platform = f'Docker/{platform}'

    return platform
