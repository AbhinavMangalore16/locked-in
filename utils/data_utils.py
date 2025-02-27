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
from datetime import datetime, timedelta
import statistics

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

def exist_user(user_data):
    try:
        user_data = user_data['userinfo']
        db = connect_db()
        db_users = db['users']

        doc = db_users.find_one({"email": user_data['email']})

        if db_users.find_one({"email": user_data['email']}):
            return user_data
        
        else:
            db_users.insert_one({'email': user_data['email'],
                                'name': user_data['name'],
                                'email_verified': user_data['email_verified']})
            return user_data

        # return user

    except Exception as e:
        logger.error(f"User Exist Error: {e}")

def find_user_by_email(email):
    db = connect_db()
    collection = db.users
    return collection.find_one({"email": email})

def insert_or_update_user(user_input):
    db = connect_db()
    collection = db.users
    email = user_input.get("email")
    name = user_input.get("name")
    
    if not email or not name:
        raise ValueError("Email and Name are required fields.")
    
    existing_user = find_user_by_email(email)
    
    user_data = {
        "age_group": statistics.median(map(int, user_input["age_group"].split('-'))) if '-' in user_input["age_group"] else user_input["age_group"],
        "current_role": user_input["current_role"],
        "industry": user_input["industry"],
        "learning_style": user_input["learning_style"]
    }
    
    if existing_user:
        new_skills = list(set(existing_user.get("skills", []) + ([user_input["skills"]] if isinstance(user_input["skills"], str) else user_input["skills"])))
        user_data["skills"] = new_skills
        collection.update_one({"email": email}, {"$set": user_data})
    else:
        user_data.update({"email": email, "name": name, "skills": user_input["skills"]})
        collection.insert_one(user_data)