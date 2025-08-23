from src.IntentClassification.components.data_ingestion import DataIngestion
from src.IntentClassification.config.configuration import ConfigurationManager
from src.IntentClassification import logger

class DataIngestionPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try:
            logger.info("Starting Data Ingestion pipeline")
            config_manager = ConfigurationManager()
            data_ingestion_config = config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(config = data_ingestion_config)
            data_ingestion.export_collection_as_csv()
            logger.info("Data Ingestion pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error occurred in Data Ingestion Pipeline: {e}")
            raise e