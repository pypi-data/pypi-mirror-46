Known issues
============
* Ubuntu Desktop 18.04 LTS (Bionic) is not supported because `libncurses5-dev` and
  some other system dependencies are not installable (looks like maintainer's bug:
  https://bugs.launchpad.net/ubuntu/+source/ncurses/+bug/1773370 and https://ubuntuforums.org/showthread.php?t=2404144
  - no googlable solutions at the time of writing). Note that Ubuntu Server 18.04 LTS (Bionic) is
  supported (it does not have this issue).
* After upgrade from Packy Agent v1 to Packy Agent v2 user will be logged out
  from Packy Agent Console (reasons: latest `itsdangerous` library calculates session cookie
  expiration differently, session cookie contains `agent_id` not `agent_key` as in newest Agent
  version)
