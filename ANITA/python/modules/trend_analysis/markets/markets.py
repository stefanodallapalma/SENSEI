import json
import os
import logging
from datetime import datetime

from ..scraper.market.enum import Market
from modules.trend_analysis.markets.local.MarketLocalProject import MarketLocalProject
from celery_task.tasks.trend_analysis import market as market_task
from utils.validators import timestamp_validator

logger = logging.getLogger("market module")


def get_markets():
    markets = [market.name.lower() for market in Market if market.value != 0]

    return 200, json.dumps(markets)


def load_dump(market, dump_zip, timestamp):
    # Preconditions
    markets = get_markets()
    if market is None or market.lower() not in markets:
        error = {"error": "Market not implemented"}
        return 404, error

    logger.info("Analysing {} dump".format(market + "-" + timestamp))

    if timestamp is None:
        # Check if the folder name contains the date
        try:
            timestamp = timestamp_validator(timestamp)
        except:
            # No valid date name. It will be generate an actual timestamp
            logger.info("Impossible to retrieve the timestamp. Generation of a new one")
            timestamp = int(datetime.now().timestamp())

    logger.info("Timestamp - {}".format(timestamp))

    market_local = MarketLocalProject(market)

    market_local.save_and_extract(dump_zip, timestamp)
    dump_raw_path = market_local.raw_path

    # Unique id
    unique_id = "-".join(["TA", market, str(timestamp), market_task.LOAD_DUMP_TASK_ID])

    market_task.load_dump()