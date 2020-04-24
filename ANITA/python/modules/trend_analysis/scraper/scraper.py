import os
import time
import logging
from datetime import datetime

# Local imports
from .market.handler import get_scraper_instance
from .market.enum import Market
from utils.validators import timestamp_validator
from utils.FileUtils import getfiles, save_json

logger = logging.getLogger("scraper")


def analyse_folder(dir_path, market, timestamp=None):
    # Preconditions
    if not os.path.isdir(dir_path):
        error = {"error": "Invalid path"}
        return 500, error

    markets = [market.name.lower() for market in Market if market.value != 0]
    if market is None or market.lower() not in markets:
        error = {"error": "Market not implemented"}
        return 404, error

    name = os.path.basename(dir_path)
    logger.info("Analysing {} {}".format(market, name))

    if timestamp is None:
        # Check if the folder name contains the date
        try:
            timestamp = timestamp_validator(name)
        except:
            # No valid date name. It will be generate an actual timestamp
            logger.info("Impossible to retrieve the timestamp. Generation of a new one")
            timestamp = int(datetime.now().timestamp())
            logger.info("Timestamp - {}".format(timestamp))




    return 200, None
