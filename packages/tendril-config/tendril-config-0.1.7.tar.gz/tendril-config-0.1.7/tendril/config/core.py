

import os
from tendril.utils.config import ConfigConstant
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = []


config_constants_basic = [
    ConfigConstant(
        'INSTANCE_ROOT',
        "os.path.join(os.path.expanduser('~'), '.tendril')",
        "Path to the tendril instance root. Can be redirected if necessary"
        "with a file named ``redirect`` in this folder."
    )
]


config_constants_redirected = [
    ConfigConstant(
        'INSTANCE_CONFIG_FILE',
        "os.path.join(INSTANCE_ROOT, 'instance_config.py')",
        'Path to the tendril instance configuration.'
    ),
    ConfigConstant(
        'LOCAL_CONFIG_FILE',
        "os.path.join(INSTANCE_ROOT, 'local_config_overrides.py')",
        'Path to local overrides to the instance configuration.'
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_constants_basic,
                          doc="Tendril Default Instance Root")

    if os.path.exists(os.path.join(manager.INSTANCE_ROOT, 'redirect')):
        logger.info("Found instance redirect")
        with open(os.path.join(manager.INSTANCE_ROOT, 'redirect'), 'r') as f:
            manager.INSTANCE_ROOT = f.read().strip()

    manager.load_elements(config_constants_redirected,
                          doc="Tendril Configuration Paths")
    manager.load_config_files()
