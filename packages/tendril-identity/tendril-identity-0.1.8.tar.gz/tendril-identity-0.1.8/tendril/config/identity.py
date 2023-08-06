

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_identity = [
    ConfigOption(
        'PRIMARY_PERSONA',
        "None",
        "The default persona to use."
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_identity,
                          doc="Identity Configuration")
