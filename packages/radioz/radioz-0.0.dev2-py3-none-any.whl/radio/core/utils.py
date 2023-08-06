"""
utils.py lugar para pequenos trechos de código que
podem ser usados em toda a aplicação.
"""

import importlib

from radio.core.log import logger


def load_plugin(path_to_plugin):
    try:
        plug = importlib.import_module(path_to_plugin)
        return plug
    except ImportError as exc:
        logger.debug(exc)
