import os
from box import ConfigBox
from pathlib import Path
import yaml
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.IntentClassification import logger
import pickle

def read_yaml(file_path: Path) -> ConfigBox:
    logger.info("Inside read_yaml method")
    try:
        logger.info(f"Reading yaml file from path: {file_path}")
        with open(file_path) as file:
            content = yaml.safe_load(file)
            logger.info(content)
            logger.info(type(content))
            logger.info("yaml file loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise e
    
def create_directories(paths: list):
    logger.info("inside create_directories method")
    try:
        for path in paths:
            os.makedirs(path, exist_ok=True)
            logger.info(f"Directory created: {path}")
    except Exception as e:
        logger.error(f"Error creating directories: {e}")
        raise e

def connect_to_mongodb():
    logger.info("inside connect_to_mongodb method")
    try:
        load_dotenv()
        client = MongoClient(os.getenv('MONGO_DB_URL'), server_api=ServerApi('1'))
        client.admin.command('ping')
        logger.info("Connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise e

def save_object(file_path, obj):
    try:
        logger.info("Inside save_object method")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logger.info(f"file saved in {file_path}")
    except Exception as e:
        logger.error(f"Error observed in save_object method:{e}")
        raise e

def load_object(file_path):
    try:
        logger.info("Inside file_path metod")
        if not os.path.exists(file_path):
            logger.info(f"file path {file_path} doesnot exist")
        else:
            with open(file_path, "rb") as file:
                return pickle.load(file)
            logger.info(f"file loaded succesfully from path {file_path}")
    except Exception as e:
        logger.error(f"error inside load_object:{e}")
        raise e
