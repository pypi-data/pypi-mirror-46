

from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_render = [
    ConfigOption(
        'DOX_TEMPLATE_FOLDER',
        "os.path.join(INSTANCE_ROOT, 'dox/templates')",
        "Path to the template folder to use for tendril.dox"
    )
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_render,
                          doc="Document Rendering Configuration")
