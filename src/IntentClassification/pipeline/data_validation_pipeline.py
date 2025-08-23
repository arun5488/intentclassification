from src.IntentClassification.components.data_validation import DataValidation
from src.IntentClassification.config.configuration import ConfigurationManager
from src.IntentClassification import logger

class DataValidationPipeline:
    def __init__(self):
        logger.info("Initializing Data Validation Pipeline")
    
    def initiate_data_validation(self):
        try:
            logger.info("Starting Data Validation pipeline")
            config_manager = ConfigurationManager()
            data_validation_config = config_manager.get_data_validation_config()
            data_validation = DataValidation(data_validation_config)
            data_validation.validate_ingested_data()
        except Exception as e:
            logger.error(f"Error occurred in Data Validation Pipeline: {e}")
            raise e