import logging

import kidx_core.version

logging.getLogger(__name__).addHandler(logging.NullHandler())

__version__ = kidx_core.version.__version__
