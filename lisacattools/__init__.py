from ._version import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __name__,
    __url__,
    __version__,
)
from .utils import FrameEnum
from .analyze import LisaAnalyse, CatalogAnalysis, HistoryAnalysis
from .catalog import LisaCatalogs, LisaCatalog
import os
import logging.config
from logging import NullHandler
from .custom_logging import (
    LogRecord,
    UtilsLogs,
)

logging.getLogger(__name__).addHandler(NullHandler())

UtilsLogs.addLoggingLevel("TRACE", 15)
try:
    PATH_TO_CONF = os.path.dirname(os.path.realpath(__file__))
    logging.config.fileConfig(os.path.join(PATH_TO_CONF, "logging.conf"))
    logging.debug(
        "file %s loaded" % os.path.join(PATH_TO_CONF, "logging.conf")
    )
except Exception as exception:  # pylint: disable=broad-except
    logging.warning("cannot load logging.conf : %s" % exception)
logging.setLogRecordFactory(LogRecord)  # pylint: disable=no-member


__all__ = [
    "LisaCatalogs",
    "LisaCatalog",
    "LisaAnalyse",
    "CatalogAnalysis",
    "HistoryAnalysis",
    "FrameEnum",
]
