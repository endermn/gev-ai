import logging

from services.logger import GevaiLogger

logger: logging.Logger = GevaiLogger(name=__name__, file="gevai.log").get_logger()
