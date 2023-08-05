

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_paths = [
    ConfigOption(
        'DOCSTORE_ROOT',
        "os.path.join(INSTANCE_ROOT, 'docstore')",
        "Folder for the docstore filesystem"
    ),
    ConfigOption(
        'REFDOC_ROOT',
        "os.path.join(INSTANCE_ROOT, 'refdocs')",
        "Folder for the refdocs filesystem"
    ),
    ConfigOption(
        'INSTANCE_CACHE',
        "os.path.join(INSTANCE_ROOT, 'cache')",
        "Folder within which the tendril instance should store it's cache(s)."
        "Make sure the the users running tendril (as well as the webserver, "
        "if the web frontend is being used) have write access to this folder."
    ),
    ConfigOption(
        'SHAREDCACHE_ROOT',
        "os.path.join(INSTANCE_CACHE, 'shared')",
        "Folder for the shared cache filesystem"
    ),
    ConfigOption(
        'AUDIT_PATH',
        "os.path.join(INSTANCE_ROOT, 'manual-audit')",
        "Folder where files generated for manual audit should be stored"
    ),
    ConfigOption(
        'SVN_ROOT',
        "os.path.join(INSTANCE_ROOT, 'projects')",
        "Common ancestor for all VCS checkout folders. While tendril will "
        "try to descend into this folder indefinitely, avoid using overly "
        "generic paths (like '/' or '~') to avoid surprises and preserve "
        "performance."
    ),
    ConfigOption(
        'PROJECTS_ROOT',
        "SVN_ROOT",
        "Common ancestor for all project folders. Use this if your projects"
        "are in a single sub-tree of your VCS_ROOT, for example. \nWhile "
        "tendril will try to descend into this folder indefinitely, avoid "
        "using overly generic paths (like '/' or '~') to avoid surprises "
        "and preserve performance."
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_paths,
                          doc="Tendril Resource Paths Configuration")
