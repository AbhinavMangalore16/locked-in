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

def main(CSV_FILE_PATH, DB_NAME, COLLECTION_NAME):
    try:
        df = pd.read_csv(CSV_FILE_PATH)

        df.reset_index(drop=True, inplace=True)
        json_data = list(json.loads(df.T.to_json()).values())

        client = pymongo.MongoClient(MONGO_URI)

        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        collection.insert_many(json_data)
        logger.info(f"Data Exported to MongoDB Successfully.")

    except Exception as e:
        logger.error(f'Data insert Error: {e}')

if __name__ == '__main__':
    try:
        File_path = r"DATASETS\Online_Courses.csv"
        Database = "hackhound-db"
        Collection = "courses"
        main(File_path, Database, Collection)

        logger.info(f"Records inserted successfully.")
    
    except Exception as e:
        logger.error(f"Error in main: {e}")