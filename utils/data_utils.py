import os
import sys
from dotenv import load_dotenv
import pymongo
import pandas as pd
import numpy as np
from urllib.parse import quote_plus
import logging
import logging.config
import json
import logging
import certifi
from utils.logs_utils import setup_logging

setup_logging("LOGS/data_export.log")
logger = logging.getLogger(__name__)

try:
    load_dotenv()
    CA = certifi.where()
    MONGO_USERNAME = quote_plus(os.getenv("MONGO_USERNAME"))
    MONGO_PASSWORD = quote_plus(os.getenv("MONGO_PASSWORD"))
    

    if not MONGO_USERNAME or not MONGO_PASSWORD:
        raise logger.debug("MongoDB credentials are not set in the .env file.")

    MONGO_URI = os.getenv("MONGO_URI")

except Exception as e:
    logger.critical(e)

def connect_db():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        logger.info("Connected to MongoDB.")
        return client['hackhound-db']

    except Exception as e:
        logger.error(f"Connection Error: {e}")
