from src.IntentClassification.entity import DataIngestionConfig
from src.IntentClassification import logger

from src.IntentClassification.utils.common import connect_to_mongodb
from dotenv import load_dotenv
import pandas as pd

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        logger.info("Initialized DataIngestion component")
        self.config = config
        self.client = connect_to_mongodb()   
    
    def export_collection_as_csv(self):
        logger.info("Inside export_collection_as_csv method")
        try:
            load_dotenv()
            logger.info("Loaded environment variables")
            csv_file_path = self.config.dataset_file_name
            logger.info(f"CSV file path: {csv_file_path}")
            database = self.config.database_name
            logger.info(f"Database name: {database}")
            collection = self.config.collection_name
            logger.info(f"Collection name: {collection}")
            db = self.client[database]
            colln=db[collection]
            logger.info("Connected to MongoDB collection successfully")
            
            df = pd.DataFrame(list(colln.find()))
            logger.info(f"export successful, total records loaded: {len(df.index)}")
            if "_id" in df.columns:
                df.drop(columns=['_id'], inplace =True, axis=1)
            if "Unnamed: 0" in df.columns:
                df.drop(columns=['Unnamed: 0'], inplace =True, axis=1)
            logger.info(f"csv_file saved succesfully at: {csv_file_path}")
            df.to_csv(csv_file_path, index=False, header = True)

        except Exception as e:
            logger.error(f"Error occurred while exporting collection to CSV: {e}")
            raise e

